from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

db = SQLAlchemy()


# commands for db
def create(obj):
    db.session.add(obj)
    status = False
    try:
        db.session.commit()
        status = True

    except IntegrityError as err:
        db.session.rollback()
        print("rollback: {}, {}".format(err.orig.diag.message_primary, err.orig.diag.message_detail))

    db.session.commit()
    return status


def update():
    db.session.commit()


def delete(obj):
    db.session.delete(obj)
    db.session.commit()
