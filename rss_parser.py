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

import spotify_tagger as spotify


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
            # Parse Track
            try:
                self.artist, self.song = self.title.split(u':\xa0')    # whitespace
            except ValueError:
                try:
                    self.artist, self.song = self.title.split(u': ')
                except ValueError:
                    try:
                        self.artist, self.song = self.title.split(u':')
                    except ValueError:
                        try:
                            self.artist, self.song = self.title.split(u'–')
                        except ValueError:
                            try:
                                self.artist, self.song = self.title.split(u';')
                            except ValueError:
                                """ if artists is empty, means parsing failed """
                                print("Error didn't extract artist from track: '{}'".format(self.title))
                                self.song = self.title

            # Spotify Match
            self.spotifyData = spotify.searchTrack(song=self.song, artist=self.artist)
            if self.spotifyData:
                print(self.spotifyData.song.id)

    def __str__(self):
        msg = "<track_{} ({})".format(self.position, self.type)
        if self.type == 'song':
            return "{} - {} / {}>".format(msg, self.artist, self.song)
        else:
            return "{} - {}>".format(msg, self.title)

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
        # self.image = soup.img.attrs['src']

        for i in soup.find_all('p'):
            if i.get_text() == "The Singers and Songs":
                i.extract()

            elif i.get_text().startswith("Read Fred Bal’s Annotations"):
                i.extract()

        # tracklist
        self.tracklist = list()
        tmp_tracklist = soup.find_all(['p', 'li'])
        position = 1
        for t in tmp_tracklist:

            if not (t.get_text() == u'\xa0' or t.get_text() == ''):
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
feeddata = feedparser.parse(feedfile)

""" Seeding episodes & tracks to the database """
with app.app_context():
    db.drop_all()
    db.create_all()

    Status.add(Status(name='matched'))
    Status.add(Status(name='pending'))
    Status.add(Status(name='unmatched'))

    for episode_data in feeddata.entries[1:]:
        myEpisode = EpisodeParser(episode_data)

        # print(myEpisode)
        # for i in myEpisode.tracklist:
        #    print(i)

        newEpisode = Episodes(**myEpisode.props_for_db())
        Episodes.add(newEpisode)

        for tag in myEpisode.tags:
            EpisodesCategories.add(EpisodesCategories(category=tag, episode_id=myEpisode.id))

        for myTrack in myEpisode.tracklist:
            newTrack = Tracks(episode_id=newEpisode.id, **myTrack.props_for_db())
            Tracks.add(newTrack)

            # TODO: maybe move song/artist to tracks table
            TracksTagQuery.add(
                TracksTagQuery(track_id=newTrack.id, song=myTrack.song, artist=myTrack.artist)
            )
