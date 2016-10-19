from flask import Flask
from flask_restful import Api
from archive.resources.episodes import *
from archive.resources.tracks import *

app = Flask(__name__)
app.config.from_object('config')

from archive.models import db
db.init_app(app)

api = Api(app)

# Episode
api.add_resource(ApiEpisode, '/api/episodes', '/api/episodes/<int:episode_id>', endpoint='episode_api')
api.add_resource(ApiTracklist, '/api/episodes/<int:episode_id>/tracklist', endpoint='tracklist_api')

# Track
api.add_resource(ApiTrack, '/api/tracks/<int:track_id>', endpoint='track_api')

import archive.views
