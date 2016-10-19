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


def searchTrack(song, artist, track_id):
    # search track
    results = search('track:{} artist:{}'.format(song, artist))
    if len(results) > 0:
        collectSpotifyData(results[0], 'track', track_id)
    else:
        # search artist
        results = search('artist:{}'.format(artist))
        if len(results) > 0:
            collectSpotifyData(results[0], 'artist', track_id)
        else:
            print("Error...didn't find track for: {} / {}".format(song, artist))


def collectSpotifyData(data, match_type, track_id):
    if match_type == 'track':
        # TODO: handle multiple artists
        myTracksData = models.TracksSpotifyData(
            track_id=track_id,
            artist_id=CollectArtistData(data['artists'][0]).id,
            album_id=CollectAlbumData(data['album']).id,
            song_id=CollectSongData(data).id
        )
    else:
        myTracksData = models.TracksSpotifyData(track_id=track_id, artist_id=CollectArtistData(data).id)

    models.TracksSpotifyData.create(myTracksData)


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

    def create(self):
        self.Model.create(self.myModel)


class CollectArtistData(BaseResource):
    def __init__(self, data):
        self.Model = models.SpotifyArtists
        super().__init__(data)
        if not data.get('images'):
            data = spotify.artist(self.id)

        self.addImage(data['images'])
        self.create()

    def __repr__(self):
        return self.id


class CollectAlbumData(BaseResource):
    def __init__(self, data):
        self.Model = models.SpotifyAlbums
        super().__init__(data)
        self.addImage(data['images'])
        self.create()


class CollectSongData(BaseResource):
    def __init__(self, data):
        self.Model = models.SpotifySongs
        super().__init__(data)
        self.myModel.preview_url = data['preview_url']
        self.addImage(data['album']['images'])
        self.create()


with app.app_context():
    for myTrack in models.Tracks.query.filter_by(resolved=True).limit(10):
        searchTrack(song=myTrack.song, artist=myTrack.artist, track_id=myTrack.id)
