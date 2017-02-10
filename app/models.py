from . import db
from sqlalchemy import func, UniqueConstraint, desc
from sqlalchemy.exc import IntegrityError
from datetime import datetime


"""
-----------------------------------------------------------------------------------------------------
Class Methods for interating with DB/Model
-----------------------------------------------------------------------------------------------------
"""


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


"""
-----------------------------------------------------------------------------------------------------
Models
-----------------------------------------------------------------------------------------------------
"""

aux_tracks_artists = db.Table(
    'aux_tracks_artists',
    db.Column('artist_id', db.String, db.ForeignKey('artists.id')),
    db.Column('track_id', db.Integer, db.ForeignKey('tracks.id'))
)

aux_songs_artists = db.Table(
    'aux_songs_artists',
    db.Column('song_id', db.String, db.ForeignKey('songs.id')),
    db.Column('artist_id', db.String, db.ForeignKey('artists.id'))
)

aux_artists_tags = db.Table(
    'aux_artists_tags',
    db.Column('artist_id', db.String, db.ForeignKey('artists.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
)


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
    spotify_artists = db.relationship('Artists', secondary=aux_tracks_artists, backref='tracks')

    UniqueConstraint(episode_id, title)

    def __repr__(self):
        return '<Track ({}): {}>'.format(self.id, self.title)


class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    def __repr__(self):
        return '<{} - {}: {}>'.format(self.id, self.__class__.__name__, self.name)

    @classmethod
    def getId(cls, name):
        return cls.query.filter_by(name=name).first().id

    # @classmethod
    # def countSong(cls):
    #     return db.session.query(Tags, func.count(Songs.id).label('track_count')) \
    #                      .join(aux_songs_tags, (aux_songs_tags.c.tag_id == Tags.id)) \
    #                      .join(Songs, Songs.id == aux_songs_tags.c.song_id) \
    #                      .group_by(Tags)


class Songs(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    preview_url = db.Column(db.String)
    artists = db.relationship('Artists', secondary=aux_songs_artists, backref='songs')

    def __repr__(self):
        return '<{} - {}: {}>'.format(self.id, self.__class__.__name__, self.name)


class Artists(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    lastfm_name = db.Column(db.String)
    lastfm_image = db.Column(db.String)
    lastfm_tags = db.relationship('Tags', secondary=aux_artists_tags, backref='artists')

    def __repr__(self):
        return '<{} - {}: {}>'.format(self.id, self.__class__.__name__, self.name)
