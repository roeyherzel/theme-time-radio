from archive.models import db
from archive.models.podcast import Tracks, Images
from archive.models.common import Mixin


class Tags(db.Model, Mixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    type = db.Column(db.String)

    def __repr__(self):
        return '<{} - {}: {}>'.format(self.id, self.__class__.__name__, self.name)

    @classmethod
    def getId(cls, name):
        return cls.query.filter_by(name=name).first().id


class Songs(db.Model, Mixin):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    url = db.Column(db.String)
    preview_url = db.Column(db.String)
    album_id = db.Column(db.String, db.ForeignKey('albums.id'))
    album = db.relationship('Albums', backref=db.backref('songs', lazy='dynamic'))

    def __repr__(self):
        return '<{} - {}: {}>'.format(self.id, self.__class__.__name__, self.name)


# 1:1 album - song
class Albums(db.Model, Mixin):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    url = db.Column(db.String)

    def __repr__(self):
        return '<{} - {}: {}>'.format(self.id, self.__class__.__name__, self.name)


class Artists(db.Model, Mixin):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    url = db.Column(db.String)
    lastfm_name = db.Column(db.String)
    lastfm_image = db.Column(db.String, db.ForeignKey(Images.url))

    def __repr__(self):
        return '<{} - {}: {}>'.format(self.id, self.__class__.__name__, self.name)


# M:M
class ArtistsTags(db.Model, Mixin):
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
    artist_id = db.Column(db.String, db.ForeignKey('artists.id'), primary_key=True)
    artists = db.relationship('Artists', backref=db.backref('tags', lazy='dynamic'))
    tag = db.relationship('Tags', backref=db.backref('artists', lazy='dynamic'))

    def __repr__(self):
        return '<{} - {}: {}>'.format(self.artist_id, self.__class__.__name__, self.tag_id)


# 1:1 track - song
class TracksSongs(db.Model, Mixin):
    track_id = db.Column(db.Integer, db.ForeignKey('tracks.id'), primary_key=True)
    song_id = db.Column(db.String, db.ForeignKey('songs.id'), primary_key=True)
    tracks = db.relationship('Tracks', backref=db.backref('spotify_song', uselist=False))
    song = db.relationship('Songs', backref=db.backref('songs_tracks', lazy='dynamic'))

    def __repr__(self):
        return '<{} - {}: {}>'.format(self.song_id, self.__class__.__name__, self.track_id)


# 1:M track - artists
class TracksArtists(db.Model, Mixin):
    track_id = db.Column(db.Integer, db.ForeignKey('tracks.id'), primary_key=True)
    artist_id = db.Column(db.String, db.ForeignKey('artists.id'), primary_key=True)
    tracks = db.relationship('Tracks', backref=db.backref('spotify_artists', lazy='dynamic'))
    artist = db.relationship('Artists', backref=db.backref('artists_tracks', lazy='dynamic'))

    def __repr__(self):
        return '<{} - {}: {}>'.format(self.artist_id, self.__class__.__name__, self.track_id)
