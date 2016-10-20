from archive.models import db
from archive.models.podcast import Tracks
from archive.models.common import Mixin, Images


class SpotifySongs(db.Model, Mixin):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, unique=True)
    image = db.Column(db.String, db.ForeignKey('images.url'))
    url = db.Column(db.String)
    preview_url = db.Column(db.String)

    def __repr__(self):
        return '<{} - {}: {}>'.format(self.id, self.__class__.__name__, self.name)


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


class TracksSpotifyData(db.Model, Mixin):
    track_id = db.Column(db.Integer, db.ForeignKey('tracks.id'), primary_key=True)
    song_id = db.Column(db.String, db.ForeignKey('spotify_songs.id'))
    album_id = db.Column(db.String, db.ForeignKey('spotify_albums.id'))
    artist_id = db.Column(db.String, db.ForeignKey('spotify_artists.id'))

    track_song = db.relationship('Tracks', backref=db.backref('spotify_song', uselist=False))
    track_album = db.relationship('Tracks', backref=db.backref('spotify_album', uselist=False))
    track_artist = db.relationship('Tracks', backref=db.backref('spotify_artist', uselist=False))

    song = db.relationship('SpotifySongs', backref=db.backref('tracks', lazy='dynamic'))
    album = db.relationship('SpotifyAlbums', backref=db.backref('tracks', lazy='dynamic'))
    artist = db.relationship('SpotifyArtists', backref=db.backref('tracks', lazy='dynamic'))
