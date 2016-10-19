from archive.models import db
from archive.models.mixin import Mixin


class TracksActions():
    def add(newTrack, tags=None):
        Mixin.add(newTrack)
        if tags:
            if type(tags) is not list:
                raise TypeError("tags must be list")
            else:
                for tag in tags:
                    Mixin.add(TracksTags(tag=tag, track_id=newTrack.id))


class TracksTags(db.Model):
    tag = db.Column(db.String(), primary_key=True)
    track_id = db.Column(db.Integer, db.ForeignKey('tracks.id'), primary_key=True)
    tracks = db.relationship('Tracks', backref=db.backref('tags', lazy='dynamic'))


class Tracks(db.Model, TracksActions):
    id = db.Column(db.Integer, primary_key=True)
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'))
    episode = db.relationship('Episodes', backref=db.backref('tracklist', lazy='dynamic'))
    title = db.Column(db.String())
    song = db.Column(db.String())
    artist = db.Column(db.String())
    position = db.Column(db.Integer)
    resolved = db.Column(db.Boolean)

    def __repr__(self):
        return '<Track ({}) - {}>'.format(self.id, self.title)
