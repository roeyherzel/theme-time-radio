from archive.models import db
from archive.models.common import CRUD


class Artists(db.Model, CRUD):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    thumb = db.Column(db.String())
    profile = db.Column(db.String())
    type = db.Column(db.String())
    real_name = db.Column(db.String())

    def __repr__(self):
        return '<Artist ({}) - {}>'.format(self.id, self.name)


class ArtistsUrls(db.Model, CRUD):
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), primary_key=True)
    artist = db.relationship('Artists', backref=db.backref('urls', lazy='dynamic'))
    url = db.Column(db.String(), primary_key=True)


class ArtistsAliases(db.Model, CRUD):
    id = db.Column(db.Integer, primary_key=True)    # NOTE: ids is discogs artist_id
    name = db.Column(db.String(), primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), primary_key=True)
    artist = db.relationship('Artists', backref=db.backref('aliases', lazy='dynamic'))


class ArtistsGroups(db.Model, CRUD):
    id = db.Column(db.Integer, primary_key=True)    # NOTE: ids is discogs artist_id
    name = db.Column(db.String(), primary_key=True)
    active = db.Column(db.Boolean())
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), primary_key=True)
    artist = db.relationship('Artists', backref=db.backref('groups', lazy='dynamic'))


class ArtistsMembers(db.Model, CRUD):
    id = db.Column(db.Integer, primary_key=True)    # NOTE: ids is discogs artist_id
    name = db.Column(db.String(), primary_key=True)
    active = db.Column(db.Boolean())
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), primary_key=True)
    artist = db.relationship('Artists', backref=db.backref('members', lazy='dynamic'))


class ArtistsImages(db.Model, CRUD):
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), primary_key=True)
    artist = db.relationship('Artists', backref=db.backref('images', lazy='dynamic'))
    type = db.Column(db.String())
    width = db.Column(db.Integer())
    height = db.Column(db.Integer())
    uri = db.Column(db.String())
    uri150 = db.Column(db.String())
    resource_url = db.Column(db.String(), unique=True)
