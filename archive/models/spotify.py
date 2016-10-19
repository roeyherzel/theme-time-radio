from archive.models import db
from archive.models.mixin import Mixin


class SpotifySongs(db.Model, Mixin):
    spotify_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, unique=True)
    image = db.Column(db.String)
    endpoint_url = db.Column(db.String)
    preview_url = db.Column(db.String)

    def __repr__(self):
        return '<SpotifySongs ({}): {}>'.format(self.spotify_id, self.name)


class SpotifyAlbums(db.Model, Mixin):
    spotify_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, unique=True)
    image = db.Column(db.String, db.ForeignKey('images.url'))
    endpoint_url = db.Column(db.String)

    def __repr__(self):
        return '<SpotifyAlbums ({}): {}>'.format(self.spotify_id, self.name)


class SpotifyArtists(db.Model, Mixin):
    spotify_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, unique=True)
    image = db.Column(db.String, db.ForeignKey('images.url'))
    endpoint_url = db.Column(db.String)

    def __repr__(self):
        return '<SpotifyArtists ({}): {}>'.format(self.spotify_id, self.name)


class TracksSpotifyData(db.Model, Mixin):
    track_id = db.Column(db.Integer, db.ForeignKey('tracks.id'), primary_key=True)
    song_id = db.Column(db.String, db.ForeignKey('spotify_songs.spotify_id'))
    album_id = db.Column(db.String, db.ForeignKey('spotify_albums.spotify_id'))
    artist_id = db.Column(db.String, db.ForeignKey('spotify_artists.spotify_id'))


class Images(db.Model, Mixin):
    url = db.Column(db.String, primary_key=True)
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)

    def __repr__(self):
        return '<Image ({}): {}>'.format(self.id, self.url)
