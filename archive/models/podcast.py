from archive.models import db
from archive.models.mixin import Mixin
from datetime import datetime


class Episodes(db.Model, Mixin):
    id = db.Column(db.Integer, primary_key=True)
    season = db.Column(db.Integer)
    title = db.Column(db.String())
    description = db.Column(db.Unicode())
    aired = db.Column(db.String())
    media = db.Column(db.String())
    image = db.Column(db.String())

    def __repr__(self):
        return '<Episode ({}): {}>'.format(self.id, self.title)


class EpisodesTags(db.Model, Mixin):
    tag = db.Column(db.String(), primary_key=True)
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'), primary_key=True)
    episode = db.relationship('Episodes', backref=db.backref('tags', lazy='dynamic'))


class Tracks(db.Model, Mixin):
    id = db.Column(db.Integer, primary_key=True)
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'))
    episode = db.relationship('Episodes', backref=db.backref('tracklist', lazy='dynamic'))
    title = db.Column(db.String())
    parsed_song = db.Column(db.String())
    parsed_artist = db.Column(db.String())
    position = db.Column(db.Integer)
    resolved = db.Column(db.Boolean)

    def __repr__(self):
        return '<Track ({}): {}>'.format(self.id, self.title)


class TracksTags(db.Model, Mixin):
    tag = db.Column(db.String(), primary_key=True)
    track_id = db.Column(db.Integer, db.ForeignKey('tracks.id'), primary_key=True)
    track = db.relationship('Tracks', backref=db.backref('tags', lazy='dynamic'))
