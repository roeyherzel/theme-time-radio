import requests
import sys
import time
import logging
import json
import unicodedata
import sqlalchemy

from archive import app, models

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

    def __init__(self, artist):
        super().__init__()
        self.url = "http://ws.audioscrobbler.com/2.0"
        self.api_key = "aa570c383c5f26de24d4e2c7fd182c8e"
        self.params = {
            'method': 'artist.getinfo',
            'api_key': self.api_key,
            'format': 'json'
        }
        self.found = False
        self.params['artist'] = artist
        self.make_request()
        if self.request.ok:
            try:
                self.data = self.request.json()['artist']
                self.found = True
            except KeyError:
                pass

    def getImage(self):
        res = [image['#text'] for image in self.data['image'] if image['size'] == 'large']
        return res[0] if res else None

    def getName(self):
        return self.data['name']

    def getTags(self):
        return [tag['name'] for tag in self.data['tags']['tag']]


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


def collectArtistData(data, trackObj):
    artistObj = models.Artists.query.get(data['id'])
    if artistObj is None:
        # removes accents like "Édith Piaf"
        artistObj = models.Artists(
            id=data['id'],
            name=unicodedata.normalize('NFKD', data['name']).encode('ASCII', 'ignore').decode()
        )
        # LastFM name must be left with accents like "Édith Piaf"
        lastfm_info = LastFM(data['name'])
        if lastfm_info.found:
            artistObj.lastfm_name = lastfm_info.getName()
            artistObj.lastfm_image = lastfm_info.getImage()

            for tag in lastfm_info.getTags():
                tagObj = models.Tags(name=tag)
                if models.create(tagObj) is False:
                    tagObj = models.Tags.query.filter(models.Tags.name == tag).one_or_none()

                logging.debug("%s", tagObj)
                artistObj.tags.append(tagObj)

        models.create(artistObj)

    trackObj.spotify_artists.append(artistObj)


def collectSongData(data, trackObj):
    songObj = models.Songs(id=data['id'], name=data['name'], preview_url=data['preview_url'])
    if models.create(songObj) is False:
        songObj = models.Songs.query.get(data['id'])

    trackObj.spotify_song_id = songObj.id


def tagTrack(song, artist, trackObj):
    logging.info("tagTrack - track_id: %s, song: %s, artist: %s", trackObj, song, artist)
    # search track
    results = Spotify(track=song, artist=artist)
    if results.found:
        collectSongData(results.data, trackObj)

        for a in results.data['artists']:
            collectArtistData(a, trackObj)
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
    with app.app_context():
        track_list = models.Tracks.query.filter(models.Tracks.spotify_song_id == None, models.Tracks.resolved == True)
        if limit:
            track_list = track_list.limit(limit)

        tag_from_query(track_list.all())
