from archive.models import db
from archive.models.common import CRUD
from datetime import datetime


class Episodes(db.Model, CRUD):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    plot = db.Column(db.String())
    description = db.Column(db.Unicode())
    guest = db.Column(db.String())
    date_pub = db.Column(db.DateTime)
    date_add = db.Column(db.DateTime)
    podcast_url = db.Column(db.String())
    thumb = db.Column(db.String())

    def __init__(self, id, title, description, guest, published, podcast, thumb, plot):
        self.id = id
        self.title = title
        self.plot = plot
        self.description = description
        self.guest = guest
        self.date_pub = published
        self.date_add = datetime.utcnow()
        self.podcast_url = podcast
        self.thumb = thumb

    def __repr__(self):
        return '<Episode ({}) - {}>'.format(self.id, self.title)
