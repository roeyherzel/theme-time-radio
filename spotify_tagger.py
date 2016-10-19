import spotipy
import sys
import time
from pprint import pprint

from archive import app, models

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


def searchTrack(song, artist):
    query = 'track:{} artist:{}'.format(song, artist)
    # search track
    items = search(query)
    if len(items) > 0:
        collectSpotifyData(items[0], 'track')
    else:
        # search artist
        query = 'artist:{}'.format(artist, 'artist')
        items = search(query)
        if len(items) > 0:
            collectSpotifyData(items[0], 'artist')
        else:
            print("Error...didn't find track for: {} / {}".format(song, artist))


def collectSpotifyData(item, match_type):
    if match_type == 'track':
        # TODO: handle multiple artists
        myArtist = Artist(item['artists'][0])
        myAlbum = Album(item['album'])
        mySong = Song(item)
        print("SpotifyData: {} {} {}".format(mySong, myArtist, myAlbum))
        myArtist.add()
        myAlbum.add()
        mySong.add()
    else:
        myArtist = Artist(item)
        myArtist.add()
        print("SpotifyData: {}".format(myArtist))


class BaseResource(object):
    def __init__(self, item):
        self.id = item['id']
        self.name = item['name']
        self.url = item['href']
        self.type = item['type']

    def __str__(self):
        return "<{}: {}>".format(self.__class__.__name__, self.name)

    def add(self):
        self.dbAddObj = self.DbClass(spotify_id=self.id, name=self.name, endpoint_url=self.url)


class Artist(BaseResource):
    def __init__(self, data):
        self.DbClass = models.SpotifyArtists
        super().__init__(data)

    def add(self):
        super().add()
        self.DbClass.add(self.dbAddObj)


class Album(BaseResource):
    def __init__(self, data):
        self.DbClass = models.SpotifyAlbums
        super().__init__(data)

    def add(self):
        super().add()
        self.DbClass.add(self.dbAddObj)


class Song(BaseResource):
    def __init__(self, data):
        self.DbClass = models.SpotifySongs
        self.preview_url = data['preview_url']
        super().__init__(data)
        self.external_ids = data.get('external_ids', None)  # only relevant for song

    def add(self):
        super().add()
        self.dbAddObj.preview_url = self.preview_url
        self.DbClass.add(self.dbAddObj)


with app.app_context():
    for myTrack in models.Tracks.query.filter_by(resolved=True).limit(10):
        # print(myTrack)
        searchTrack(song=myTrack.song, artist=myTrack.artist)
