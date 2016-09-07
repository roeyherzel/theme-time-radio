
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import event, desc, distinct

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

    def __repr__(self):
        return '<Status ({}) - {}>'.format(self.id, self.name)

    @classmethod
    def getIdByName(cls, name):
        return cls.query.filter_by(name=name).first().id

    @classmethod
    def getNameById(cls, id):
        return cls.query.filter_by(id=id).first().name


class Episodes(db.Model, CRUD):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    plot = db.Column(db.String())
    description = db.Column(db.Unicode())
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

    def __repr__(self):
        return '<Episode ({}) - {}>'.format(self.id, self.title)


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

    def __repr__(self):
        return '<Track ({}) - {}>'.format(self.id, self.title)


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
    aggregated = db.Column(db.Integer, db.ForeignKey('status.id'))

    def __init__(self, track_id, song=None, release=None, artist=None):
        self.track_id = track_id
        self.song = song or Status.getIdByName('unmatched')
        self.release = release or Status.getIdByName('unmatched')
        self.artist = artist or Status.getIdByName('unmatched')
        self.aggregated = Status.getIdByName('unmatched')


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

    def __repr__(self):
        return '<Artist ({}) - {}>'.format(self.id, self.name)


class Releases(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    thumb = db.Column(db.String())
    year = db.Column(db.Integer())
    # styles
    # genres
    # images

    def __repr__(self):
        return '<Release ({}) - {}>'.format(self.id, self.title)


class Songs(db.Model):
    id = db.Column(db.String(), primary_key=True)
    title = db.Column(db.String())
    position = db.Column(db.String())
    type = db.Column(db.String())
    duration = db.Column(db.String())
    release_id = db.Column(db.Integer, db.ForeignKey('releases.id'))
    release = db.relationship('Releases', backref=db.backref('songs', lazy='dynamic'))

    def __repr__(self):
        return '<Song ({}) - {}>'.format(self.id, self.title)


class TracksArtists(db.Model):
    __tablename__ = 'tracks_artists'

    track_id = db.Column(db.Integer, db.ForeignKey('tracks.id'), primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), primary_key=True)
    status = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)
    track = db.relationship('Tracks', backref=db.backref('artist_tags', lazy='dynamic'))
    artist = db.relationship('Artists', backref=db.backref('tracks', lazy='dynamic'))

    def __init__(self, track_id, artist_id, status):
        self.track_id = track_id
        self.artist_id = artist_id
        self.status = status

    def __repr__(self):
        return '<TracksArtists track({}) - artist({})>'.format(self.track_id, self.artist_id)


class TracksReleases(db.Model):
    __tablename__ = 'tracks_releases'

    track_id = db.Column(db.Integer, db.ForeignKey('tracks.id'), primary_key=True)
    release_id = db.Column(db.Integer, db.ForeignKey('releases.id'), primary_key=True)
    status = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)
    track = db.relationship('Tracks', backref=db.backref('release_tags', lazy='dynamic'))
    release = db.relationship('Releases', backref=db.backref('tracks', lazy='dynamic'))

    def __init__(self, track_id, release_id, status):
        self.track_id = track_id
        self.release_id = release_id
        self.status = status

    def __repr__(self):
        return '<TracksReleases track({}) - release({})>'.format(self.track_id, self.release_id)


class TracksSongs(db.Model):
    __tablename__ = 'tracks_songs'

    track_id = db.Column(db.Integer, db.ForeignKey('tracks.id'), primary_key=True)
    song_id = db.Column(db.String(), db.ForeignKey('songs.id'), primary_key=True)
    status = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)
    track = db.relationship('Tracks', backref=db.backref('song_tags', lazy='dynamic'))
    song = db.relationship('Songs', backref=db.backref('tracks', lazy='dynamic'))

    def __init__(self, track_id, song_id, status):
        self.track_id = track_id
        self.song_id = song_id
        self.status = status

    def __repr__(self):
        return '<TracksSongs track({}) - song({})>'.format(self.track_id, self.song_id)


@db.event.listens_for(Tracks, "after_insert")
def insert_tag_status(mapper, connection, target):
    tag_status = TracksTagStatus(track_id=target.id)
    db.session.add(tag_status)


@db.event.listens_for(TracksArtists, "after_insert")
@db.event.listens_for(TracksReleases, "after_insert")
@db.event.listens_for(TracksSongs, "after_insert")
def update_resource_tag_status(mapper, connection, target):
    table = TracksTagStatus.__table__
    mapped_table_name = mapper.mapped_table.name

    if mapped_table_name == 'tracks_artists':
        connection.execute(
            table.update().where(table.c.track_id == target.track_id).values(artist=target.status)
        )
    elif mapped_table_name == 'tracks_releases':
        connection.execute(
            table.update().where(table.c.track_id == target.track_id).values(release=target.status)
        )
    elif mapped_table_name == 'tracks_songs':
        connection.execute(
            table.update().where(table.c.track_id == target.track_id).values(song=target.status)
        )

    # calc and update aggregated status
    track_tag_status = TracksTagStatus.query.get(target.track_id).__dict__
    values = [track_tag_status[i] for i in ['song', 'release', 'artist']]

    # pending
    if Status.getIdByName('pending') in values:
        agg_status = Status.getIdByName('pending')

    # full-matched
    elif len(list(filter(lambda x: x == Status.getIdByName('matched'), values))) == 3:
        agg_status = Status.getIdByName('full-matched')

    # half-matched
    elif track_tag_status['artist'] == Status.getIdByName('matched') and \
            track_tag_status['release'] != Status.getIdByName('matched'):
        agg_status = Status.getIdByName('half-matched')

    # unmatched
    else:
        agg_status = Status.getIdByName('unmatched')

    connection.execute(
        table.update().where(table.c.track_id == target.track_id).values(aggregated=agg_status)
    )
