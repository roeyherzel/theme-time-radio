from archive.models import db, Artists
from archive.models import CRUD


class Albums(db.Model, CRUD):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    type = db.Column(db.String())

    def __repr__(self):
        return '<Album ({}) - {}>'.format(self.id, self.name)


class AlbumsArtists(db.Model, CRUD):
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'), primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), unique=True)
    album = db.relationship('Albums', backref=db.backref('artists', lazy='dynamic'))
    artist = db.relationship('Artists', backref=db.backref('albums', lazy='dynamic'))


class AlbumsGenres(db.Model, CRUD):
    genre = db.Column(db.String(), primary_key=True)
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'), primary_key=True)
    album = db.relationship('Albums', backref=db.backref('genres', lazy='dynamic'))
