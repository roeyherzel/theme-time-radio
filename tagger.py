import requests
import sys
import time
import logging
import json
import unicodedata
import sqlalchemy

from app import create_app, models

logging.getLogger("requests").setLevel(logging.WARNING)
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', filename='tagging.log', level=logging.DEBUG)


class BaseAPI(object):
    def __init__(self):
        self.params = {}
        self.headers = {}

    def make_request(self):
        try:
            self.request = requests.get(self.url, params=self.params, headers=self.headers)

        except requests.exceptions.ConnectionError as err:
            logging.error("[%s] - %s...retry in 2 sec", self.__class__, err)
            time.sleep(2)
            self.request = requests.get(self.url, params=self.params, headers=self.headers)

        logging.debug("make_request - %s", self.request.url)


class LastFM(BaseAPI):

    def __init__(self):
        super().__init__()
        self.url = "http://ws.audioscrobbler.com/2.0"
        self.api_key = "aa570c383c5f26de24d4e2c7fd182c8e"
        self.params = {
            'api_key': self.api_key,
            'format': 'json',
            'autocorrect': 1
        }

    def getArtistInfo(self, artist):
        self.found = False
        self.data = dict()
        self.params['method'] = 'artist.getinfo'
        self.params['artist'] = artist

        self.make_request()
        if self.request.ok:
            try:
                data = self.request.json()['artist']
                # name
                self.data['name'] = data['name']
                # image
                res = [image['#text'] for image in data['image'] if image['size'] == 'extralarge']
                self.data['image'] = res[0] if res else None
                self.found = True

            except KeyError:
                pass

    def getTrackInfo(self, track, artist):
        self.found = False
        self.data = dict()
        self.params['method'] = 'track.getinfo'
        self.params['track'] = track
        self.params['artist'] = artist

        self.make_request()
        if self.request.ok:
            try:
                data = self.request.json()['track']
                self.data['tags'] = [tag['name'] for tag in data['toptags']['tag']]
                self.found = True

            except KeyError:
                pass


class Spotify(BaseAPI):

    def __init__(self, artist, track=None):
        super().__init__()
        self.url = "https://api.spotify.com/v1/search"
        self.headers = {'Accept': 'application/json'}
        self.params = {'limit': 1}
        self.found = False

        if track:
            self.params['q'] = "track:{} artist:{}".format(track, artist)
            self.params['type'] = 'track'
        else:
            self.params['q'] = "artist:{}".format(artist)
            self.params['type'] = 'artist'

        self.make_request()
        if self.request.ok:
            types = "{}s".format(self.params['type'])
            try:
                self.data = self.request.json()[types]['items'][0]
                self.found = True
            except (KeyError, IndexError):
                pass


def collectArtistData(data, trackObj, songObj=None):
    artistObj = models.Artists.query.get(data['id'])
    if artistObj is None:
        # removes accents like "Édith Piaf"
        artistObj = models.Artists(
            id=data['id'],
            name=unicodedata.normalize('NFKD', data['name']).encode('ASCII', 'ignore').decode()
        )
        # LastFM name must be left with accents like "Édith Piaf"
        lastfm = LastFM()
        lastfm.getArtistInfo(data['name'])
        if lastfm.found:
            artistObj.lastfm_name = lastfm.data['name']
            artistObj.lastfm_image = lastfm.data['image']

        models.create(artistObj)

    trackObj.spotify_artists.append(artistObj)
    if songObj:
        songObj.artists.append(artistObj)


def collectSongData(data, trackObj):
    songObj = models.Songs(id=data['id'], name=data['name'], preview_url=data['preview_url'])
    if models.create(songObj) is False:
        songObj = models.Songs.query.get(data['id'])

    trackObj.spotify_song_id = songObj.id

    for artist_data in data['artists']:
        collectSongTags(songObj, artist_data['name'])
        collectArtistData(artist_data, trackObj, songObj)


def collectSongTags(songObj, artist):
    lastfm = LastFM()
    lastfm.getTrackInfo(track=songObj.name, artist=artist)

    if lastfm.found:
        for tag in lastfm.data['tags']:
            tagObj = models.Tags(name=tag)

            if models.create(tagObj) is False:
                tagObj = models.Tags.query.filter(models.Tags.name == tag).one_or_none()

            logging.debug("%s", tagObj)
            songObj.tags.append(tagObj)


def tagTrack(song, artist, trackObj):
    logging.info("tagTrack - track_id: %s, song: %s, artist: %s", trackObj, song, artist)
    # search track
    results = Spotify(track=song, artist=artist)
    if results.found:
        collectSongData(results.data, trackObj)
    else:
        # search artist
        results = Spotify(artist=artist)
        if results.found:
            logging.warning("ONLY ARTIST")
            collectArtistData(results.data, trackObj)
        else:
            logging.error("didn't find track for: %s / %s", song, artist)


def tag_from_query(track_list):
    logging.info("--- Tagging #%s Tracks", len(track_list))
    for track in track_list:
        tagTrack(song=track.parsed_song, artist=track.parsed_artist, trackObj=track)


def tag_all_unresolved_untagged(limit=None):
    with create_app().app_context():
        track_list = models.Tracks.query.filter(models.Tracks.spotify_song_id == None, models.Tracks.resolved == True)
        if limit:
            track_list = track_list.limit(limit)

        tag_from_query(track_list.all())
