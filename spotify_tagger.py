import spotipy
import requests
import pylast
import sys
import time
from pprint import pprint

from archive import app, models


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
        self.request = requests.get(__class__.API_URL, params=query_params)
        self.found = False
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

    except spotipy.client.SpotifyException as err:
        print(err, "sleeping 2 sec")
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
            print("ONLY ARTIST")
            collectSpotifyData(results[0], 'artist', track_id)
        else:
            print("Error...didn't find track for: {} / {}".format(song, artist))


def collectSpotifyData(data, match_type, track_id):
    if match_type == 'track':
        mySong = models.TracksSongs(track_id=track_id, song_id=CollectSongData(data).id)
        models.Mixin.create(mySong)
        print(mySong)

        # NOTE: data['artists'] had too many artists
        for artist in data['album']['artists']:
            myArtist = models.TracksArtists(track_id=track_id, artist_id=CollectArtistData(artist).id)
            models.Mixin.create(myArtist)
            print(myArtist)
    else:
        myArtist = models.TracksArtists(track_id=track_id, artist_id=CollectArtistData(data).id)
        models.Mixin.create(myArtist)
        print(myArtist)


class BaseResource(object):
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.url = data['href']
        self.type = data['type']
        self.myModel = self.Model(id=self.id, name=self.name, url=self.url)

    def __str__(self):
        return "<{}: {}>".format(self.__class__.__name__, self.name)

    def create(self):
        models.Mixin.create(self.myModel)
        print(self.myModel, end='\n')


class CollectArtistData(BaseResource):
    def __init__(self, data):
        self.Model = models.Artists
        super().__init__(data)

        artistInfo = LastFMArtist(self.myModel.name)
        if artistInfo.found:
            image = artistInfo.getImage()
            models.Mixin.create(models.Images(url=image))
            self.myModel.lastfm_name = artistInfo.getName()
            self.myModel.lastfm_image = image

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


with app.app_context():
    models.ArtistsTags.query.delete()
    models.TracksSongs.query.delete()
    models.TracksArtists.query.delete()
    models.Songs.query.delete()
    models.Albums.query.delete()
    models.Artists.query.delete()
    models.db.session.commit()

    for myTrack in models.Tracks.query.filter_by(resolved=True).limit(50):
        print("\n" + str(myTrack))
        searchTrack(song=myTrack.parsed_song, artist=myTrack.parsed_artist, track_id=myTrack.id)
