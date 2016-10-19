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
    # search track
    results = search('track:{} artist:{}'.format(song, artist))
    if len(results) > 0:
        collectSpotifyData(results[0], 'track')
    else:
        # search artist
        results = search('artist:{}'.format(artist))
        if len(results) > 0:
            collectSpotifyData(results[0], 'artist')
        else:
            print("Error...didn't find track for: {} / {}".format(song, artist))


def collectSpotifyData(item, match_type):
    if match_type == 'track':
        # TODO: handle multiple artists
        CollectArtistData(item['artists'][0])
        CollectAlbumData(item['album'])
        CollectSongData(item)
    else:
        CollectArtistData(item)


class BaseResource(object):
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.url = data['href']
        self.type = data['type']

        self.myModel = self.Model(spotify_id=self.id, name=self.name, endpoint_url=self.url)
        print(self.myModel)

    def __str__(self):
        return "<{}: {}>".format(self.__class__.__name__, self.name)

    def addImage(self, images):
        image = images[0]
        models.Images.create(models.Images(**image))
        self.myModel.image = image['url']


class CollectArtistData(BaseResource):
    def __init__(self, data):
        self.Model = models.SpotifyArtists
        super().__init__(data)
        if not data.get('images'):
            data = spotify.artist(self.id)

        self.addImage(data['images'])
        self.Model.create(self.myModel)


class CollectAlbumData(BaseResource):
    def __init__(self, data):
        self.Model = models.SpotifyAlbums
        super().__init__(data)
        self.addImage(data['images'])
        self.Model.create(self.myModel)


class CollectSongData(BaseResource):
    def __init__(self, data):
        self.Model = models.SpotifySongs
        self.external_ids = data.get('external_ids', None)  # only relevant for song
        super().__init__(data)
        self.myModel.preview_url = data['preview_url']
        self.addImage(data['album']['images'])
        self.Model.create(self.myModel)


with app.app_context():
    for myTrack in models.Tracks.query.filter_by(resolved=True).limit(10):
        searchTrack(song=myTrack.song, artist=myTrack.artist)
