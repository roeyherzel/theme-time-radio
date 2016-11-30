from . import db
from sqlalchemy import func, UniqueConstraint, desc
from sqlalchemy.exc import IntegrityError
from datetime import datetime


""" commands for db """


def create(obj):
    db.session.add(obj)
    status = False
    try:
        db.session.commit()
        status = True

    except IntegrityError as err:
        db.session.rollback()
        print("rollback: {}, {}".format(err.orig.diag.message_primary, err.orig.diag.message_detail))

    db.session.commit()
    return status


def update():
    db.session.commit()


def delete(obj):
    db.session.delete(obj)
    db.session.commit()


""" Models """


class Episodes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    season = db.Column(db.Integer)
    title = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.Unicode())
    aired = db.Column(db.String)
    media = db.Column(db.String)
    image = db.Column(db.String)

    @property
    def next(self):
        return Episodes.query.filter(Episodes.id > self.id).order_by(Episodes.id).first()

    @property
    def prev(self):
        return Episodes.query.filter(Episodes.id < self.id).order_by(desc(Episodes.id)).first()

    def __repr__(self):
        return '<Episode ({}): {}>'.format(self.id, self.title)


association_track_artists = db.Table(
    'association_track_artists',
    db.Column('artist_id', db.String, db.ForeignKey('artists.id')),
    db.Column('track_id', db.Integer, db.ForeignKey('tracks.id'))
)


class Tracks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    episode_id = db.Column(db.Integer, db.ForeignKey(Episodes.id), nullable=False)
    episode = db.relationship('Episodes', backref=db.backref('tracklist', lazy='dynamic'))
    title = db.Column(db.String(), nullable=False)
    parsed_song = db.Column(db.String())
    parsed_artist = db.Column(db.String())
    position = db.Column(db.Integer)
    year = db.Column(db.Integer)
    resolved = db.Column(db.Boolean)

    spotify_song_id = db.Column(db.String, db.ForeignKey('songs.id'))
    spotify_song = db.relationship('Songs', uselist=False, backref='tracks')
    spotify_artists = db.relationship('Artists', secondary=association_track_artists, backref='tracks')

    UniqueConstraint(episode_id, title)

    def __repr__(self):
        return '<Track ({}): {}>'.format(self.id, self.title)


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
        return db.session.query(Tags, func.count(Tracks.id).label('track_count')) \
                         .join(association_artist_tags, (association_artist_tags.c.tag_id == Tags.id)) \
                         .join(association_track_artists, (association_track_artists.c.artist_id == association_artist_tags.c.artist_id)) \
                         .join(Tracks, (Tracks.id == association_track_artists.c.track_id)) \
                         .filter(Tracks.spotify_song_id != None) \
                         .group_by(Tags)


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


association_artist_tags = db.Table(
    'association_artist_tags',
    db.Column('artist_id', db.String, db.ForeignKey('artists.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
)


class Artists(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    lastfm_name = db.Column(db.String)
    lastfm_image = db.Column(db.String)
    tags = db.relationship('Tags', secondary=association_artist_tags, backref='artists')

    def __repr__(self):
        return '<{} - {}: {}>'.format(self.id, self.__class__.__name__, self.name)
