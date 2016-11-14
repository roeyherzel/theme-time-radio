from archive.models import db
from archive.models.podcast import Tracks
from sqlalchemy import func


class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    type = db.Column(db.String)

    def __repr__(self):
        return '<{} - {}: {}>'.format(self.id, self.__class__.__name__, self.name)

    @classmethod
    def getId(cls, name):
        return cls.query.filter_by(name=name).first().id

    @classmethod
    def getAllValid(cls):
        # NOTE: WORKAROUND: issue with spotifyPlayer with more then 70 songs
        return db.session.query(Tags, func.count(Tracks.id).label('track_count')) \
                         .join(ArtistsTags, (ArtistsTags.tag_id == Tags.id)) \
                         .join(TracksArtists, (TracksArtists.artist_id == ArtistsTags.artist_id)) \
                         .join(Tracks, (Tracks.id == TracksArtists.track_id)) \
                         .filter(Tracks.spotify_song) \
                         .group_by(Tags) \
                         .having(func.count(Tracks.id) <= 70) \
                         .having(func.count(Tracks.id) >= 5)


# 1:1 album - song
class Albums(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    def __repr__(self):
        return '<{} - {}: {}>'.format(self.id, self.__class__.__name__, self.name)


class Songs(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    preview_url = db.Column(db.String)
    album_id = db.Column(db.String, db.ForeignKey(Albums.id))
    album = db.relationship('Albums', backref=db.backref('songs', lazy='dynamic'))

    def __repr__(self):
        return '<{} - {}: {}>'.format(self.id, self.__class__.__name__, self.name)


class Artists(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    lastfm_name = db.Column(db.String)
    lastfm_image = db.Column(db.String)

    def __repr__(self):
        return '<{} - {}: {}>'.format(self.id, self.__class__.__name__, self.name)


# M:M
class ArtistsTags(db.Model):
    tag_id = db.Column(db.Integer, db.ForeignKey(Tags.id), primary_key=True)
    artist_id = db.Column(db.String, db.ForeignKey(Artists.id), primary_key=True)
    artists = db.relationship('Artists', backref=db.backref('tags', lazy='dynamic'))
    tag = db.relationship('Tags', backref=db.backref('artists', lazy='dynamic'))

    def __repr__(self):
        return '<{} - {}: {}>'.format(self.artist_id, self.__class__.__name__, self.tag_id)


# 1:1 track - song
class TracksSongs(db.Model):
    track_id = db.Column(db.Integer, db.ForeignKey(Tracks.id), primary_key=True)
    song_id = db.Column(db.String, db.ForeignKey(Songs.id), primary_key=True)
    tracks = db.relationship('Tracks', backref=db.backref('spotify_song', uselist=False))
    song = db.relationship('Songs', backref=db.backref('songs_tracks', lazy='dynamic'))

    def __repr__(self):
        return '<{} - {}: {}>'.format(self.song_id, self.__class__.__name__, self.track_id)


# 1:M track - artists
class TracksArtists(db.Model):
    track_id = db.Column(db.Integer, db.ForeignKey(Tracks.id), primary_key=True)
    artist_id = db.Column(db.String, db.ForeignKey(Artists.id), primary_key=True)
    tracks = db.relationship('Tracks', backref=db.backref('spotify_artists', lazy='dynamic'))
    artist = db.relationship('Artists', backref=db.backref('artists_tracks', lazy='dynamic'))

    def __repr__(self):
        return '<{} - {}: {}>'.format(self.artist_id, self.__class__.__name__, self.track_id)
