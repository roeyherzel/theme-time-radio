import spotipy
import requests
import sys
import time
from archive import app, models
import logging

logging.getLogger("requests").setLevel(logging.WARNING)
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', filename='tagging.log', level=logging.INFO)


class LastFMArtist(object):
    API_URL = "http://ws.audioscrobbler.com/2.0"
    API_KEY = "aa570c383c5f26de24d4e2c7fd182c8e"
    API_SECRET = "3b70ec5f61f6557930bab54d89f72a21"

    url_params = {
        'method': 'artist.getinfo',
        'api_key': API_KEY,
        'format': 'json'
    }

    def __init__(self, name):
        query_params = __class__.url_params
        query_params['artist'] = name
        self.found = False
        try:
            self.request = requests.get(__class__.API_URL, params=query_params)

        except requests.exceptions.ConnectionError as err:
            logging.error(err.args)
            logging.error("%s...sleeping 2 sec", err)
            time.sleep(2)
            self.request = requests.get(__class__.API_URL, params=query_params)

        if not self.request.ok:
            return
        try:
            self.data = self.request.json()['artist']
        except KeyError:
            return

        self.found = True

    def getImage(self):
        res = [image['#text'] for image in self.data['image'] if image['size'] == 'large']
        if res:
            return res[0]
        else:
            return None

    def getName(self):
        return self.data['name']

    def getTags(self):
        return [tag['name'] for tag in self.data['tags']['tag']]


spotify = spotipy.Spotify()


def search(query):
    query_type = 'track' if 'track' in query else 'artist'
    try:
        res = spotify.search(q=query, type=query_type)

    except (spotipy.client.SpotifyException, requests.exceptions.ConnectionError) as err:
        logging.error(err.args)
        logging.error("%s...sleeping 2 sec", err)
        time.sleep(2)
        res = spotify.search(q=query, type=query_type)

    return res[query_type + 's']['items']


def searchTrack(song, artist, track_id):
    # search track
    results = search('track:{} artist:{}'.format(song, artist))
    if len(results) > 0:
        collectSpotifyData(results[0], 'track', track_id)
    else:
        # search artist
        results = search('artist:{}'.format(artist))
        if len(results) > 0:
            logging.warning("ONLY ARTIST")
            collectSpotifyData(results[0], 'artist', track_id)
        else:
            logging.error("didn't find track for: %s / %s", song, artist)


def collectSpotifyData(data, match_type, track_id):
    if match_type == 'track':
        mySong = models.TracksSongs(track_id=track_id, song_id=CollectSongData(data).id)
        models.Mixin.create(mySong)
        logging.debug(mySong)

        for artist in data['album']['artists']:
            myArtist = models.TracksArtists(track_id=track_id, artist_id=CollectArtistData(artist).id)
            models.Mixin.create(myArtist)
            logging.debug(myArtist)
    else:
        myArtist = models.TracksArtists(track_id=track_id, artist_id=CollectArtistData(data).id)
        models.Mixin.create(myArtist)
        logging.debug(myArtist)


class BaseResource(object):
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.type = data['type']
        self.myModel = self.Model(id=self.id, name=self.name)

    def __str__(self):
        return "<{}: {}>".format(self.__class__.__name__, self.name)

    def create(self):
        models.Mixin.create(self.myModel)
        logging.debug(self.myModel)


class CollectArtistData(BaseResource):
    def __init__(self, data):
        self.Model = models.Artists
        super().__init__(data)

        artistInfo = LastFMArtist(self.myModel.name)
        if artistInfo.found:
            self.myModel.lastfm_name = artistInfo.getName()
            self.myModel.lastfm_image = artistInfo.getImage()

        self.create()

        if artistInfo.found:
            for tag in artistInfo.getTags():
                models.Mixin.create(models.spotify.Tags(name=tag))
                models.Mixin.create(models.ArtistsTags(tag_id=models.Tags.getId(tag), artist_id=self.myModel.id))

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
        self.myModel.preview_url = data['preview_url']
        self.myModel.album_id = CollectAlbumData(data['album']).id
        self.create()


def trackQuerySearch(arg):
    for myTrack in arg:
        logging.debug(myTrack)
        searchTrack(song=myTrack.parsed_song, artist=myTrack.parsed_artist, track_id=myTrack.id)


def db_query():
    with app.app_context():
        track_list = models.Tracks.query.filter(models.Tracks.spotify_artists == None, models.Tracks.resolved == True).all()
        logging.info("Tagging #%d Tracks", len(track_list))
        trackQuerySearch(track_list)
