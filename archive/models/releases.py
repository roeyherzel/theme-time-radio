from archive.models import db, Artists
from archive.models import CRUD


class Releases(db.Model, CRUD):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    thumb = db.Column(db.String())
    year = db.Column(db.Integer())

    def __repr__(self):
        return '<Release ({}) - {}>'.format(self.id, self.title)


class ReleasesArtists(db.Model, CRUD):
    release_id = db.Column(db.Integer, db.ForeignKey('releases.id'), primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), unique=True)
    release = db.relationship('Releases', backref=db.backref('artists', lazy='dynamic'))
    artist = db.relationship('Artists', backref=db.backref('releases', lazy='dynamic'))


class ReleasesGenres(db.Model, CRUD):
    genre = db.Column(db.String(), primary_key=True)
    release_id = db.Column(db.Integer, db.ForeignKey('releases.id'), primary_key=True)
    release = db.relationship('Releases', backref=db.backref('genres', lazy='dynamic'))


class ReleasesStyles(db.Model, CRUD):
    style = db.Column(db.String(), primary_key=True)
    release_id = db.Column(db.Integer, db.ForeignKey('releases.id'), primary_key=True)
    release = db.relationship('Releases', backref=db.backref('styles', lazy='dynamic'))


class ReleasesImages(db.Model, CRUD):
    id = db.Column(db.Integer, primary_key=True)
    release_id = db.Column(db.Integer, db.ForeignKey('releases.id'), primary_key=True)
    release = db.relationship('Releases', backref=db.backref('images', lazy='dynamic'))
    type = db.Column(db.String())
    width = db.Column(db.Integer())
    height = db.Column(db.Integer())
    uri = db.Column(db.String())
    uri150 = db.Column(db.String())
    resource_url = db.Column(db.String(), unique=True)
