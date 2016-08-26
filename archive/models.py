from marshmallow_jsonapi import Schema, fields
from marshmallow import validate  #, fields, Schema
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)

    def __init__(self, name):
        self.name = name

    @classmethod
    def getByName(cls, name):
        return cls.query.filter_by(name=name).first().id


class Episodes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    description = db.Column(db.String())
    guest = db.Column(db.String())
    date_pub = db.Column(db.DateTime)
    date_add = db.Column(db.DateTime)
    podcast_url = db.Column(db.String())

    def __init__(self, id, title, description, guest, published, podcast):
        self.id = id
        self.title = title
        self.description = description
        self.guest = guest
        self.date_pub = published
        self.date_add = datetime.utcnow()
        self.podcast_url = podcast


class EpisodesSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')
    id = fields.Integer(dump_only=True)
    # title = fields.Str()
    # description = fields.Str()
    # guest = fields.Str()
    # date_pub = fields.Time()
    # date_add = fields.Time()
    podcast_url = fields.Url()

    class Meta:
        type_ = 'episode'


class Tracks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    position = db.Column(db.Integer)
    resolved = db.Column(db.Boolean)
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'))
    episode = db.relationship('Episodes', backref=db.backref('tracks', lazy='dynamic'))

    def __init__(self, title, position, resolved, episode_id):
        self.title = title
        self.position = position
        self.resolved = resolved
        self.episode_id = episode_id


class TracksTagQuery(db.Model):
    __tablename__ = 'tracks_tag_query'

    track_id = db.Column(db.Integer, db.ForeignKey('tracks.id'), primary_key=True)
    track = db.relationship('Tracks', backref=db.backref('query', lazy='dynamic'), cascade='delete')
    song = db.Column(db.String())
    release = db.Column(db.String())
    artist = db.Column(db.String())


class TracksTagStatus(db.Model):
    __tablename__ = 'track_tag_status'

    track_id = db.Column(db.Integer, db.ForeignKey('tracks.id'), primary_key=True)
    song = db.Column(db.Integer, db.ForeignKey('status.id'))
    release = db.Column(db.Integer, db.ForeignKey('status.id'))
    artist = db.Column(db.Integer, db.ForeignKey('status.id'))


class Artists(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    thumb = db.Column(db.String())
    profile = db.Column(db.String())
    type = db.Column(db.String())
    real_name = db.Column(db.String())
    # images
    # groups
    # urls
    # members
    # aliases


class TracksArtists(db.Model):
    __tablename__ = 'tracks_artists'

    track_id = db.Column(db.Integer, db.ForeignKey('tracks.id'), primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), primary_key=True)
    status = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)
    track = db.relationship('Tracks', backref=db.backref('artists', lazy='dynamic'))
    artist = db.relationship('Artists', backref=db.backref('tracks', lazy='dynamic'))

    def __init__(self, track_id, artist_id, status):
        self.track_id = track_id
        self.artist_id = artist_id
        self.status = status


class Releases(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    thumb = db.Column(db.String())
    year = db.Column(db.Integer())
    # styles
    # genres
    # images


class TracksReleases(db.Model):
    __tablename__ = 'tracks_releases'

    track_id = db.Column(db.Integer, db.ForeignKey('tracks.id'), primary_key=True)
    release_id = db.Column(db.Integer, db.ForeignKey('releases.id'), primary_key=True)
    status = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)
    track = db.relationship('Tracks', backref=db.backref('releases', lazy='dynamic'))
    release = db.relationship('Releases', backref=db.backref('tracks', lazy='dynamic'))

    def __init__(self, track_id, release_id, status):
        self.track_id = track_id
        self.release_id = release_id
        self.status = status


class Songs(db.Model):
    id = db.Column(db.String(), primary_key=True)
    title = db.Column(db.String())
    position = db.Column(db.String())
    type = db.Column(db.String())
    duration = db.Column(db.String())
    release_id = db.Column(db.Integer, db.ForeignKey('releases.id'))
    release = db.relationship('Releases', backref=db.backref('songs', lazy='dynamic'))


class TracksSongs(db.Model):
    __tablename__ = 'tracks_songs'

    track_id = db.Column(db.Integer, db.ForeignKey('tracks.id'), primary_key=True)
    song_id = db.Column(db.String(), db.ForeignKey('songs.id'), primary_key=True)
    status = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)
    track = db.relationship('Tracks', backref=db.backref('songs', lazy='dynamic'))
    song = db.relationship('Songs', backref=db.backref('tracks', lazy='dynamic'))

    def __init__(self, track_id, song_id, status):
        self.track_id = track_id
        self.song_id = song_id
        self.status = status
