import requests
import sys
import time
from archive import app, models
import logging
import json

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


class BaseResource(object):
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.type = data['type']
        self.newModel = self.Model(id=self.id, name=self.name)

    def __str__(self):
        return "<{}: {}>".format(self.__name__, self.name)

    def create(self):
        models.create(self.newModel)
        logging.debug(self.newModel)


class CollectArtistData(BaseResource):
    def __init__(self, data):
        self.Model = models.Artists
        super().__init__(data)

        artistInfo = LastFM(self.newModel.name)
        if artistInfo.found:
            self.newModel.lastfm_name = artistInfo.getName()
            self.newModel.lastfm_image = artistInfo.getImage()

        self.create()

        if artistInfo.found:
            for tag in artistInfo.getTags():
                models.create(models.spotify.Tags(name=tag))
                models.create(models.ArtistsTags(tag_id=models.Tags.getId(tag), artist_id=self.newModel.id))

    def __repr__(self):
        return self.id


class CollectAlbumData(BaseResource):
    def __init__(self, data):
        self.Model = models.Albums
        super().__init__(data)
        self.create()


class CollectSongData(BaseResource):
    def __init__(self, data):
        self.Model = models.Songs
        super().__init__(data)
        self.newModel.preview_url = data['preview_url']
        self.newModel.album_id = CollectAlbumData(data['album']).id
        self.create()


def tagTrack(song, artist, track_id):
    logging.info("tagTrack - track_id: %d, song: %s, artist: %s", track_id, song, artist)
    # search track
    results = Spotify(track=song, artist=artist)
    if results.found:
        newSong = models.TracksSongs(track_id=track_id, song_id=CollectSongData(results.data).id)
        models.create(newSong)
        logging.debug(newSong)

        for artist in results.data['artists']:
            newArtist = models.TracksArtists(track_id=track_id, artist_id=CollectArtistData(artist).id)
            models.create(newArtist)
            logging.debug(newArtist)
    else:
        # search artist
        results = Spotify(artist=artist)
        if results.found:
            logging.warning("ONLY ARTIST")
            newArtist = models.TracksArtists(track_id=track_id, artist_id=CollectArtistData(results.data).id)
            models.create(newArtist)
            logging.debug(newArtist)
        else:
            logging.error("didn't find track for: %s / %s", song, artist)


def tag_from_query(arg):
    logging.info("Tagging #%d Tracks", len(arg))
    for myTrack in arg:
        logging.debug(myTrack)
        tagTrack(song=myTrack.parsed_song, artist=myTrack.parsed_artist, track_id=myTrack.id)


def tag_all_unresolved_tagged(limit=None):
    with app.app_context():
        track_list = models.Tracks.query.filter(models.Tracks.spotify_artists == None, models.Tracks.resolved == True)
        if limit:
            track_list = track_list.limit(limit)

        tag_from_query(track_list.all())
