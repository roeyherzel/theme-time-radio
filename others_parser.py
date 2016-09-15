#!/usr/local/bin/python3

import feedparser
import re
import json
import time
import discogs_tagger as tagger
from bs4 import BeautifulSoup
from bidi.algorithm import get_display

from alphabet_detector import AlphabetDetector
ad = AlphabetDetector()

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-file", type=str, help="rss feed file to process")
parser.add_argument("-num", type=int, help="number of episodes to process")
parser.add_argument("-index", type=int, help="episode index to process")
args = parser.parse_args()

# defaults
feed_files = ['download.xml', 'download2.xml']

if args.file:
    feed_files = [args.file]


def set_args(episodes_feed_list):
    print(args)
    if args.num:
        return episodes_feed_list[0:args.num]
    if args.index:
        return list(episodes_feed_list[args.index])

    return episodes_feed_list

# ' - '
SYMB_dash = b' \xe2\x80\x93 '

# ' מתוך '
HEB_from = b' \xd7\x9e\xd7\xaa\xd7\x95\xd7\x9a '

# ' כל השירים בתכנית של'
HEB_artist_for_all = b'\xd7\x9b\xd7\x9c \
\xd7\x94\xd7\xa9\xd7\x99\xd7\xa8\xd7\x99\xd7\x9d \
\xd7\x91\xd7\xaa\xd7\x9b\xd7\xa0\xd7\x99\xd7\xaa \
\xd7\xa9\xd7\x9c '

# 'שיחה עם'
HEB_conversation_with = b'\xd7\xa9\xd7\x99\xd7\x97\xd7\x94 \xd7\xa2\xd7\x9d'

# 'התארח באולפן:'
HEB_guest_in_studio = b'\xd7\x94\xd7\xaa\xd7\x90\xd7\xa8\xd7\x97 \
\xd7\x91\xd7\x90\xd7\x95\xd7\x9c\xd7\xa4\xd7\x9f'

# 'להאזנה לתכנית'
HEB_listen_to_show = b'\xd7\x9c\xd7\x94\xd7\x90\xd7\x96\xd7\xa0\xd7\x94 \
\xd7\x9c\xd7\xaa\xd7\x9b\xd7\xa0\xd7\x99\xd7\xaa'

# regex for hebrew words
regex_artist_for_all = re.compile(r'' + HEB_artist_for_all.decode() + r'(.*?)(\.$|$)')
regex_guest_in_studio = re.compile(r'' + HEB_guest_in_studio.decode() + r'(\s|:)(.*?)(\.$|$)')
regex_conversation_with = re.compile(r'' + HEB_conversation_with.decode() + r'(\s|:)(.*?)(\.$|$)')
regex_listen_to_show = re.compile(r'' + HEB_listen_to_show.decode() + r'.*?')


def RTL(var):
    var = get_display(var)  # hebrew RTL
    return var


def track_massage(string):
    # remove "\xc2\xa0" kaki (hidden space)
    string = re.sub(b"\xc2\xa0", b' ', string.encode()).decode()

    # fix right-to-left issues
    if string.startswith('['):
        if re.search(HEB_from.decode(), string):
            string = re.sub(r'^\[(.*?)(' + HEB_from.decode() + ')', r'\1]\2', string)
        else:
            string = re.sub(r'^\[(.*?)$', r'\1]', string)

    elif string.startswith('('):
        if re.search(HEB_from.decode(), string):
            string = re.sub(r'^\((.*?)(' + HEB_from.decode() + ')', r'\1)\2', string)
        else:
            string = re.sub(r'^\((.*?)$', r'\1)', string)

    elif string.startswith('?'):
        string = re.sub(r'^\?(.*?)$', r'\1?', string)

    elif string.startswith('!'):
        string = re.sub(r'^\!(.*?)$', r'\1!', string)

    return string


class Track():
    def __init__(self, title, position, artist_for_all=None):
        """ Parse original track title into Artist/Release/Title """
        self.title = track_massage(title)
        self.position = position

        self.resolved = False
        self.query = dict([(i, None) for i in ['song', 'release', 'artist']])

        # try to resolve release
        releaseSplit = self.title.encode().split(HEB_from)
        if len(releaseSplit) == 2:
            self.query['release'] = releaseSplit[1].decode().strip()
            self.resolved = True

        self.query['song'] = releaseSplit[0]

        # try to resolve artist
        artistSplit = self.query['song'].split(SYMB_dash)
        if len(artistSplit) == 2:
            self.query['artist'] = artistSplit[0].decode().strip()
            self.query['song'] = artistSplit[1]
            self.resolved = True

        if artist_for_all and not self.query['artist']:
            self.query['artist'] = artist_for_all
            self.resolved = True

        if not self.resolved:
            self.query['song'] = None
        else:
            self.query['song'] = self.query['song'].decode().strip()

        self.tag = tagger.tagTrack(self.query['song'],
                                   self.query['release'],
                                   self.query['artist'])

    def __str__(self):
        return "original: {}\ntrack  : {}\nrelease: {}\nartist : {}\n".format(self.title,
                                                                              self.query['song'],
                                                                              self.query['release'],
                                                                              self.query['artist'])

def categories_filter(cat):
    if cat.isdigit():
        return False

    elif cat in ['ספטמבר', 'אוגוסט', 'יולי', 'יוני', 'מאי', 'אפריל', 'מרץ', 'פברואר', 'ינואר', 'דצמבר', 'נובמבר', 'אוקטובר']:
        return False
    else:
        return True


class Episode():
    def __init__(self, ep):
        self.id = int(re.sub(r'http://others\.co\.il/\?p=(.*?)$', r'\1', ep.id))
        self.title = ep.title
        self.image = ep.img
        self.podcast_link = ep.links[1].href
        self.published = ep.published_parsed
        self.categories = list(filter(categories_filter, [t.term for t in ep.tags]))
        self.guest = None
        self._artist_for_all = None

        print("Episode: {}".format(RTL(self.title)))

        # parse plot
        soup = BeautifulSoup(ep.description, 'html.parser')
        if soup.a:
            soup.a.extract()

        clean_plot = re.search(r'(?P<plot>.*?)_{2,}', soup.text)
        self.plot = clean_plot.group('plot') if clean_plot else soup.text

        # parse body
        soup = BeautifulSoup(ep.content[0].value, 'html.parser')
        playlist_info = soup.ul.findPrevious('p').extract().text
        ul = soup.ul.extract()

        # parse platlist info
        if not (playlist_info.startswith('_') or playlist_info == ''):

            # look for guest in studio
            res = regex_guest_in_studio.search(playlist_info)
            if res:
                self.guest = res.group(2).strip()
            else:
                # look for conversation with
                res = regex_conversation_with.search(playlist_info)
                if res:
                    self.guest = res.group(2).strip()

            # look for artist for all tracks (only latin chars for now)
            res = regex_artist_for_all.search(playlist_info)
            if res and ad.is_latin(res.group(1)):
                self._artist_for_all = res.group(1)

        # clean and collect description
        description = soup.text.split('\n')
        description.append('\n' + playlist_info)
        description = [line for line in description
                       if not (line == '' or
                               line.startswith('_') or
                               line.startswith('\n_') or
                               regex_listen_to_show.search(line))]

        self.description = '\n'.join(description)

        # collect tracks from playlist
        position = 1
        self.playlist = list()
        for t in [i.text for i in ul.find_all('li')]:
            print('~~~~~~~~~~~~~~~~~~~')

            myTrack = Track(t, position, self._artist_for_all)
            self.playlist.append(myTrack)
            position += 1

            print(myTrack)
            print(myTrack.tag)

        print('=' * 50)


for feed in feed_files:
    data = set_args(feedparser.parse(feed).entries)
    ep_list = list()

    for ep in data:
        myEpisode = Episode(ep)
        ep_list.append(myEpisode)
        print("--------------\n")

    with open('db.json', 'w') as f:
        f.write(json.dumps({'episodes': ep_list},
                default=lambda x: x.__dict__, ensure_ascii=False))
