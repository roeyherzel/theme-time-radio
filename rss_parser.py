#!/usr/local/bin/python3.5

import feedparser
from bs4 import BeautifulSoup
import re
import json
from pprint import pprint

from archive import app
from archive.models import *

import sqlalchemy
from datetime import datetime


def strptime(timestap_list):
    timestamp_str = ' '.join([str(i) for i in timestap_list[0:6]])
    return datetime.strptime(timestamp_str, "%Y %m %d %H %M %S")


class TrackParser(object):
    def __init__(self, data, position):
        self.artist, self.album, self.song = None, None, None
        self.type = "talk" if data.name == 'p' else "song"
        self.title = data.get_text()
        self.position = position

        if self.type == "song":
            res = self.title.split(u':\xa0')    # whitespace
            if len(res) == 2:
                self.artist, self.song = res
            else:
                res = self.title.split(u': ')
                self.artist, self.song = res    # NOTE: this one could raise assert

    def __str__(self):
        if self.type == 'song':
            msg = "{} / {}".format(self.type, self.artist, self.song)
            return "<track_{} ({}) - {} / {}>".format(self.position, self.type, self.artist, self.song)
        else:
            return "<track_{} ({}) - {}>".format(self.position, self.type, self.title)

    def props_for_db(self):
        return {
            'title': self.title,
            'position': self.position,
            'type': self.type,
        }


class EpisodeParser(object):
    def __init__(self, data):
        self.title = data.title
        self.published_date = data.published_parsed
        self.description = data.summary
        self.image = None

        self.tags = [t['term'] for t in data.tags]
        self.id = int(re.sub(r'http://www\.themetimeradio\.com/\?p=(.*?)$', r'\1', data.id))
        self.media_link = list(filter(lambda x: x.type == 'audio/mpeg', data.links))[0].href

        # parse html content using 'lxml' because it's faster
        soup = BeautifulSoup(data.content[0].value, 'lxml')

        # cleanup
        for s in soup.find_all('script'):
            s.parent.extract()

        # extract image, and some more cleanup
        for i in soup.find_all('p'):
            if i.get_text() == "The Singers and Songs":
                self.image = i.img.attrs['src']
                i.extract()

            elif i.get_text().startswith("Read Fred Bal’s Annotations") or i.get_text() == u'\xa0':    # whitespace
                i.extract()

        # tracklist
        self.tracklist = list()
        tmp_tracklist = soup.find_all(['p', 'li'])
        position = 1
        for t in tmp_tracklist:
            self.tracklist.append(TrackParser(t, position))
            position += 1

    def __str__(self):
        return "<episode {} - {}>".format(self.id, self.title)

    def props_for_db(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'date_pub': strptime(self.published_date),
            'podcast_url': self.media_link,
            'thumb': self.image,
        }

"""
Show's info/description: data.entries[0]
Episodes starts at: data.entries[1]
"""
feedfile = "theme_time_radio_hour.rss"
data = feedparser.parse(feedfile)

episode_data = data.entries[1]
myEpisode = EpisodeParser(episode_data)

print(myEpisode)
for i in myEpisode.tracklist:
    print(i)


""" Seeding episodes & tracks to the database """
with app.app_context():
    db.drop_all()
    db.create_all()

    Status.add(Status(name='matched'))
    Status.add(Status(name='pending'))
    Status.add(Status(name='unmatched'))

    newEpisode = Episodes(**myEpisode.props_for_db())
    Episodes.add(newEpisode)

    for tag in myEpisode.tags:
        EpisodesCategories.add(EpisodesCategories(category=tag, episode_id=myEpisode.id))

    for myTrack in myEpisode.tracklist:
        newTrack = Tracks(episode_id=newEpisode.id, **myTrack.props_for_db())
        Tracks.add(newTrack)
        TracksTagQuery.add(
            TracksTagQuery(track_id=newTrack.id, song=myTrack.song, artist=myTrack.artist)
        )
