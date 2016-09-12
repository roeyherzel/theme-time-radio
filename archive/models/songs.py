from archive.models import db
from archive.models.common import CRUD


class Songs(db.Model, CRUD):
    id = db.Column(db.String(), primary_key=True)
    title = db.Column(db.String())
    position = db.Column(db.String())
    type = db.Column(db.String())
    duration = db.Column(db.String())
    release_id = db.Column(db.Integer, db.ForeignKey('releases.id'))
    release = db.relationship('Releases', backref=db.backref('songs', lazy='dynamic'))

    def __repr__(self):
        return '<Song ({}) - {}>'.format(self.id, self.title)
