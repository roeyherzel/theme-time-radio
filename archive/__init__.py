from flask import Flask
from flask_restful import Api
from archive.resources.podcast import EpisodesAPI, EpisodesTracklistAPI

app = Flask(__name__)
app.config.from_object('config')

from archive.models import db
db.init_app(app)

api = Api(app)

# Episode
api.add_resource(EpisodesAPI, '/api/episodes', '/api/episodes/<int:episode_id>', endpoint='episodes_api')
api.add_resource(EpisodesTracklistAPI, '/api/episodes/<int:episode_id>/tracklist', endpoint='episodes_tracklist_api')


import archive.views
