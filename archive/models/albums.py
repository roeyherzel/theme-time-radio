from archive.models import db, Artists
from archive.models import CRUD


class Albums(db.Model, CRUD):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    thumb = db.Column(db.String(), unique=True)
    year = db.Column(db.Integer())

    def __repr__(self):
        return '<Album ({}) - {}>'.format(self.id, self.title)


class AlbumsArtists(db.Model, CRUD):
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'), primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), unique=True)
    album = db.relationship('Albums', backref=db.backref('artists', lazy='dynamic'))
    artist = db.relationship('Artists', backref=db.backref('albums', lazy='dynamic'))


class AlbumsGenres(db.Model, CRUD):
    genre = db.Column(db.String(), primary_key=True)
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'), primary_key=True)
    album = db.relationship('Albums', backref=db.backref('genres', lazy='dynamic'))


class AlbumsStyles(db.Model, CRUD):
    style = db.Column(db.String(), primary_key=True)
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'), primary_key=True)
    album = db.relationship('Albums', backref=db.backref('styles', lazy='dynamic'))


class AlbumsImages(db.Model, CRUD):
    id = db.Column(db.Integer, primary_key=True)
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'), primary_key=True)
    album = db.relationship('Albums', backref=db.backref('images', lazy='dynamic'))
    type = db.Column(db.String())
    width = db.Column(db.Integer())
    height = db.Column(db.Integer())
    uri = db.Column(db.String())
    uri150 = db.Column(db.String())
    resource_url = db.Column(db.String(), unique=True)
