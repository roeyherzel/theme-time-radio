from archive.models import db
from archive.models.podcast import Tracks
from archive.models.common import Mixin, Images


class SpotifySongs(db.Model, Mixin):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, unique=True)
    url = db.Column(db.String)
    preview_url = db.Column(db.String)
    album_id = db.Column(db.String, db.ForeignKey('spotify_albums.id'))
    album = db.relationship('SpotifyAlbums', backref=db.backref('songs', lazy='dynamic'))

    def __repr__(self):
        return '<{} - {}: {}>'.format(self.id, self.__class__.__name__, self.name)


# 1:1 album - song
class SpotifyAlbums(db.Model, Mixin):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, unique=True)
    image = db.Column(db.String, db.ForeignKey('images.url'))
    url = db.Column(db.String)

    def __repr__(self):
        return '<{} - {}: {}>'.format(self.id, self.__class__.__name__, self.name)


class SpotifyArtists(db.Model, Mixin):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, unique=True)
    image = db.Column(db.String, db.ForeignKey('images.url'))
    url = db.Column(db.String)

    def __repr__(self):
        return '<{} - {}: {}>'.format(self.id, self.__class__.__name__, self.name)


# 1:1 track - song
class TracksSpotifySongs(db.Model, Mixin):
    track_id = db.Column(db.Integer, db.ForeignKey('tracks.id'), primary_key=True)
    song_id = db.Column(db.String, db.ForeignKey('spotify_songs.id'), primary_key=True)
    tracks = db.relationship('Tracks', backref=db.backref('spotify_song', uselist=False))
    data = db.relationship('SpotifySongs', backref=db.backref('tracks', lazy='dynamic'))

    def __repr__(self):
        return '<{} - {}: {}>'.format(self.song_id, self.__class__.__name__, self.track_id)


# 1:M track - artists
class TracksSpotifyArtists(db.Model, Mixin):
    track_id = db.Column(db.Integer, db.ForeignKey('tracks.id'), primary_key=True)
    artist_id = db.Column(db.String, db.ForeignKey('spotify_artists.id'), primary_key=True)
    tracks = db.relationship('Tracks', backref=db.backref('spotify_artists'))
    data = db.relationship('SpotifyArtists', backref=db.backref('tracks', lazy='dynamic'))

    def __repr__(self):
        return '<{} - {}: {}>'.format(self.artist_id, self.__class__.__name__, self.track_id)
