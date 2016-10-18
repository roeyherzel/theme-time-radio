from archive.models import *


class Tracks(db.Model, CRUD):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    song = db.Column(db.String())
    artist = db.Column(db.String())
    position = db.Column(db.Integer)
    type = db.Column(db.String)
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'))
    episode = db.relationship('Episodes', backref=db.backref('tracklist', lazy='dynamic'))

    def __repr__(self):
        return '<Track ({}) - {}>'.format(self.id, self.title)


class TracksTagStatus(db.Model):
    __tablename__ = 'tracks_tag_status'

    track_id = db.Column(db.Integer, db.ForeignKey('tracks.id'), primary_key=True)
    track = db.relationship('Tracks', backref=db.backref('tags_status', lazy='dynamic'), cascade='delete')
    song = db.Column(db.Integer, db.ForeignKey('status.id'))
    album = db.Column(db.Integer, db.ForeignKey('status.id'))
    artist = db.Column(db.Integer, db.ForeignKey('status.id'))
    aggregated = db.Column(db.Integer, db.ForeignKey('status.id'))

    def __init__(self, track_id, song=None, album=None, artist=None):
        self.track_id = track_id
        self.song = song or Status.getIdByName('unmatched')
        self.album = album or Status.getIdByName('unmatched')
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
