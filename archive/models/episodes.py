from archive.models import db
from archive.models.common import CRUD
from datetime import datetime


class Episodes(db.Model, CRUD):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    description = db.Column(db.Unicode())
    date_pub = db.Column(db.DateTime)
    podcast_url = db.Column(db.String())
    thumb = db.Column(db.String())

    def __repr__(self):
        return '<Episode ({}) - {}>'.format(self.id, self.title)


class EpisodesTags(db.Model, CRUD):
    tag = db.Column(db.String(), primary_key=True)
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'), primary_key=True)
    episodes = db.relationship('Episodes', backref=db.backref('tags', lazy='dynamic'))
