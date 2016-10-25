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
            print("ONLY ARTIST")
            collectSpotifyData(results[0], 'artist', track_id)
        else:
            print("Error...didn't find track for: {} / {}".format(song, artist))


def collectSpotifyData(data, match_type, track_id):
    if match_type == 'track':
        mySong = models.TracksSpotifySongs(track_id=track_id, song_id=CollectSongData(data).id)
        models.Mixin.create(mySong)
        print(mySong)

        for artist in data['artists']:
            myArtist = models.TracksSpotifyArtists(track_id=track_id, artist_id=CollectArtistData(artist).id)
            models.Mixin.create(myArtist)
            print(myArtist)
    else:
        myArtist = models.TracksSpotifyArtists(track_id=track_id, artist_id=CollectArtistData(data).id)
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

    def addImage(self, images):
        try:
            image = images[0]
        except IndexError:
            return
        models.Mixin.create(models.Images(**image))
        self.myModel.image = image['url']

    def create(self):
        models.Mixin.create(self.myModel)
        print(self.myModel, end='\n')


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
        self.myModel.album_id = CollectAlbumData(data['album']).id
        self.create()


with app.app_context():
    models.TracksSpotifySongs.query.delete()
    models.TracksSpotifyArtists.query.delete()
    models.db.session.commit()

    for myTrack in models.Tracks.query.filter_by(resolved=True).limit(50):
        print("\n" + str(myTrack))
        searchTrack(song=myTrack.parsed_song, artist=myTrack.parsed_artist, track_id=myTrack.id)
