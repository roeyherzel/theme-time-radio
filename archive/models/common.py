from archive.models import db
from sqlalchemy.exc import IntegrityError


class CRUD():

    def create(resource):
        db.session.add(resource)
        try:
            db.session.commit()
            # NOTE: enable on debug
            # print("create-commited")

        except IntegrityError as err:
            db.session.rollback()
            print("create-rollback: {}, {}".format(err.orig.diag.message_primary,
                                                   err.orig.diag.message_details))

        db.session.commit()

    def update(resource):
        db.session.commit()

    def delete(resource):
        db.session.delete(resource)
        db.session.commit()


class Status(db.Model, CRUD):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Status ({}) - {}>'.format(self.id, self.name)

    @classmethod
    def getIdByName(cls, name):
        return cls.query.filter_by(name=name).first().id

    @classmethod
    def getNameById(cls, id):
        return cls.query.filter_by(id=id).first().name
