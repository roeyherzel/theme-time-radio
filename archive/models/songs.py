from archive.models import db
from archive.models.common import CRUD


class Songs(db.Model, CRUD):
    id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String())
    type = db.Column(db.String())
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'))
    album = db.relationship('Albums', backref=db.backref('songs', lazy='dynamic'))

    def __repr__(self):
        return '<Song ({}) - {}>'.format(self.id, self.name)
