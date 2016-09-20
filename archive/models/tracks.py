from archive.models import *


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


class TracksArtists(db.Model, CRUD):
    __tablename__ = 'tracks_artists'

    track_id = db.Column(db.Integer, db.ForeignKey('tracks.id'), primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), primary_key=True)
    status = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)
    track = db.relationship('Tracks', backref=db.backref('tags_artist', lazy='dynamic'))
    artist = db.relationship('Artists', backref=db.backref('tracks', lazy='dynamic'))

    def __init__(self, track_id, artist_id, status):
        self.track_id = track_id
        self.artist_id = artist_id
        self.status = status

    def __repr__(self):
        return '<TracksArtists track({}) - artist({})>'.format(self.track_id, self.artist_id)


class TracksReleases(db.Model, CRUD):
    __tablename__ = 'tracks_releases'

    track_id = db.Column(db.Integer, db.ForeignKey('tracks.id'), primary_key=True)
    release_id = db.Column(db.Integer, db.ForeignKey('releases.id'), primary_key=True)
    status = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)
    track = db.relationship('Tracks', backref=db.backref('tags_release', lazy='dynamic'))
    release = db.relationship('Releases', backref=db.backref('tracks', lazy='dynamic'))

    def __init__(self, track_id, release_id, status):
        self.track_id = track_id
        self.release_id = release_id
        self.status = status

    def __repr__(self):
        return '<TracksReleases track({}) - release({})>'.format(self.track_id, self.release_id)


class TracksSongs(db.Model, CRUD):
    __tablename__ = 'tracks_songs'

    track_id = db.Column(db.Integer, db.ForeignKey('tracks.id'), primary_key=True)
    song_id = db.Column(db.String(), db.ForeignKey('songs.id'), primary_key=True)
    status = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)
    track = db.relationship('Tracks', backref=db.backref('tags_song', lazy='dynamic'))
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
