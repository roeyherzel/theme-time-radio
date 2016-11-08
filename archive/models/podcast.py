from archive.models import db
from archive.models.common import Mixin
from datetime import datetime

from sqlalchemy import UniqueConstraint


class Episodes(db.Model, Mixin):
    id = db.Column(db.Integer, primary_key=True)
    season = db.Column(db.Integer)
    title = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.Unicode())
    aired = db.Column(db.String)
    media = db.Column(db.String)
    image = db.Column(db.String)

    def __repr__(self):
        return '<Episode ({}): {}>'.format(self.id, self.title)


class Tracks(db.Model, Mixin):
    id = db.Column(db.Integer, primary_key=True)
    episode_id = db.Column(db.Integer, db.ForeignKey(Episodes.id))
    episode = db.relationship('Episodes', backref=db.backref('tracklist', lazy='dynamic'))
    title = db.Column(db.String(), nullable=False)
    parsed_song = db.Column(db.String())
    parsed_artist = db.Column(db.String())
    position = db.Column(db.Integer)
    year = db.Column(db.Integer)
    resolved = db.Column(db.Boolean)

    UniqueConstraint(episode_id, title)

    def __repr__(self):
        return '<Track ({}): {}>'.format(self.id, self.title)
