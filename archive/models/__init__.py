from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event, desc, distinct
from sqlalchemy.exc import IntegrityError
from datetime import datetime

db = SQLAlchemy()

# only importing for use of use in shell context
from archive.models.spotify import *
from archive.models.podcast import *


# commands for db
def create(obj):
    db.session.add(obj)
    status = 'add'
    try:
        db.session.commit()

    except IntegrityError as err:
        db.session.rollback()
        print("rollback: {}, {}".format(err.orig.diag.message_primary, err.orig.diag.message_detail))
        status = 'rollback'

    db.session.commit()
    return status


def update(obj):
    db.session.commit()


def delete(obj):
    db.session.delete(obj)
    db.session.commit()


def merge(obj):
    db.session.merge(obj)
    db.session.commit()
