#!/usr/local/bin/python3

import feedparser
from bs4 import BeautifulSoup
import re
import json
from pprint import pprint

"""
Show's info/description: data.entries[0]
Episodes starts at: data.entries[1]
"""


class Track(object):
    def __init__(self, data, track_type):
        self.track_type = track_type
        self.artist, self.album, self.song = '', '', ''
        self.title = data.encode('utf-8')

        if track_type == "song":
            res = self.title.split(b':\xc2\xa0')
            if len(res) == 2:
                self.artist, self.song = res
            else:
                res = self.title.decode('utf-8').split(u': ')
                self.artist = res[0].encode('utf-8')
                self.song = res[1].encode('utf-8')

    def __str__(self):
        if self.track_type == 'song':
            msg = "{} / {}".format(self.track_type, self.artist, self.song)
            return "<track ({}) - {} / {}>".format(self.track_type, self.artist, self.song)
        else:
            return "<track ({}) - {}>".format(self.track_type, self.title)


class Episode(object):
    def __init__(self, data):
        self.title = data.title
        self.published_date = data.published_parsed
        self.tags = [t['term'] for t in data.tags]
        self.id = int(re.sub(r'http://www\.themetimeradio\.com/\?p=(.*?)$', r'\1', data.id))
        self.description = data.summary
        self.media_link = list(filter(lambda x: x.type == 'audio/mpeg', data.links))[0].href

        soup = BeautifulSoup(data.content[0].value, 'html.parser')
        episode_image = soup.img.attrs['src']

        self.tracklist = list()
        tmp_tracklist = soup.find_all(['p', 'li'])

        position = 0
        for t in tmp_tracklist:
            if t.name == 'p' and t.text.encode('utf-8').startswith(b'\xe2\x80\x9c'):
                self.tracklist.append(Track(t.text, 'talk'))

            elif t.name == 'li':
                self.tracklist.append(Track(t.text, 'song'))

    def __str__(self):
        return "<episode {} - {}>".format(self.id, self.title)


feedfile = "theme_time_radio_hour.rss"
data = feedparser.parse(feedfile)
episode_data = data.entries[1]

myEpisode = Episode(episode_data)

print(myEpisode)
for i in myEpisode.tracklist:
    print(i)
