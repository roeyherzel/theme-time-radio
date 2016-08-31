
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import event

db = SQLAlchemy()


class CRUD():

    def create(resource):
        db.session.add(resource)
        db.session.commit()

    def update(resource):
        db.session.commit()

    def delete(resource):
        db.session.delete(resource)
        db.session.commit()


class Status(db.Model, CRUD):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)

    def __init__(self, name):
        self.name = name

    @classmethod
    def getByName(cls, name):
        return cls.query.filter_by(name=name).first().id


class Episodes(db.Model, CRUD):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    plot = db.Column(db.String())
    description = db.Column(db.String())
    guest = db.Column(db.String())
    date_pub = db.Column(db.DateTime)
    date_add = db.Column(db.DateTime)
    podcast_url = db.Column(db.String())
    thumb = db.Column(db.String())

    def __init__(self, id, title, description, guest, published, podcast, thumb, plot):
        self.id = id
        self.title = title
        self.plot = plot
        self.description = description
        self.guest = guest
        self.date_pub = published
        self.date_add = datetime.utcnow()
        self.podcast_url = podcast
        self.thumb = thumb


class Tracks(db.Model, CRUD):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    position = db.Column(db.Integer)
    resolved = db.Column(db.Boolean)
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'))
    episode = db.relationship('Episodes', backref=db.backref('tracklist', lazy='dynamic'))

    def __init__(self, title, position, resolved, episode_id):
        self.title = title
        self.position = position
        self.resolved = resolved
        self.episode_id = episode_id


class TracksTagQuery(db.Model, CRUD):
    __tablename__ = 'tracks_tag_query'

    track_id = db.Column(db.Integer, db.ForeignKey('tracks.id'), primary_key=True)
    track = db.relationship('Tracks', backref=db.backref('tags_query', lazy='dynamic'), cascade='delete')
    song = db.Column(db.String())
    release = db.Column(db.String())
    artist = db.Column(db.String())


class TracksTagStatus(db.Model):
    __tablename__ = 'tracks_tag_status'

    track_id = db.Column(db.Integer, db.ForeignKey('tracks.id'), primary_key=True)
    track = db.relationship('Tracks', backref=db.backref('tags_status', lazy='dynamic'), cascade='delete')
    song = db.Column(db.Integer, db.ForeignKey('status.id'))
    release = db.Column(db.Integer, db.ForeignKey('status.id'))
    artist = db.Column(db.Integer, db.ForeignKey('status.id'))

    def __init__(self, track_id, song=None, release=None, artist=None):
        if song is None:
            song = Status.getByName('unmatched')
        if release is None:
            release = Status.getByName('unmatched')
        if artist is None:
            artist = Status.getByName('unmatched')

        self.track_id = track_id
        self.song = song
        self.release = release
        self.artist = artist


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


class Releases(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    thumb = db.Column(db.String())
    year = db.Column(db.Integer())
    # styles
    # genres
    # images


class Songs(db.Model):
    id = db.Column(db.String(), primary_key=True)
    title = db.Column(db.String())
    position = db.Column(db.String())
    type = db.Column(db.String())
    duration = db.Column(db.String())
    release_id = db.Column(db.Integer, db.ForeignKey('releases.id'))
    release = db.relationship('Releases', backref=db.backref('songs', lazy='dynamic'))


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


@db.event.listens_for(Tracks, "after_insert")
def insert_tag_status(mapper, connection, target):
    tag_status = TracksTagStatus(track_id=target.id)
    db.session.add(tag_status)


@db.event.listens_for(TracksArtists, "after_insert")
@db.event.listens_for(TracksReleases, "after_insert")
@db.event.listens_for(TracksSongs, "after_insert")
def update_artist_tag_status(mapper, connection, target):
    dst_table = TracksTagStatus.__table__
    src_table_name = mapper.mapped_table.name

    if src_table_name == 'tracks_artists':
        connection.execute(
            dst_table.update().where(dst_table.c.track_id == target.track_id).values(artist=target.status)
        )
    elif src_table_name == 'tracks_releases':
        connection.execute(
            dst_table.update().where(dst_table.c.track_id == target.track_id).values(release=target.status)
        )
    elif src_table_name == 'tracks_songs':
        connection.execute(
            dst_table.update().where(dst_table.c.track_id == target.track_id).values(song=target.status)
        )
