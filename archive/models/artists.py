from archive.models import db
from archive.models.common import CRUD


class Artists(db.Model, CRUD):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    type = db.Column(db.String())

    def __repr__(self):
        return '<Artist ({}) - {}>'.format(self.id, self.name)
