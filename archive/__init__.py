from flask import Flask
from flask_restful import Api
from archive.resources.podcast import EpisodesAPI, EpisodesTracklistAPI
from archive.resources.spotify import ArtistsAPI, ArtistsTracksAPI

app = Flask(__name__)
app.config.from_object('config')

from archive.models import db
db.init_app(app)

api = Api(app)

# Episode
api.add_resource(EpisodesAPI, '/api/episodes', '/api/episodes/<int:episode_id>', endpoint='episodes_api')
api.add_resource(EpisodesTracklistAPI, '/api/episodes/<int:episode_id>/tracklist', endpoint='episodes_tracklist_api')

# Artist
api.add_resource(ArtistsAPI, '/api/artists', '/api/artists/<string:artist_id>', endpoint='artists_api')
api.add_resource(ArtistsTracksAPI, '/api/artists/<string:artist_id>/tracklist', endpoint='artists_tracks_api')

import archive.views
