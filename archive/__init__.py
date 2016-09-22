from flask import Flask
from flask_restful import Api
from archive.resources.episodes import *
from archive.resources.artists import *
from archive.resources.releases import *
from archive.resources.songs import *

app = Flask(__name__)
app.config.from_object('config')

from archive.models import db
db.init_app(app)

api = Api(app)

# Episode
api.add_resource(EpisodeApi, '/api/episodes', '/api/episodes/<int:episode_id>', endpoint='episode_api')
api.add_resource(TracklistApi, '/api/episodes/<int:episode_id>/tracklist', endpoint='tracklist_api')

# Artist
api.add_resource(ArtistApi, '/api/artists', '/api/artists/<int:artist_id>', endpoint='artist_api')
api.add_resource(ArtistsReleasesApi, '/api/artists/<int:artist_id>/releases', endpoint='artist_releases_api')
api.add_resource(ArtistsEpisodesApi, '/api/artists/<int:artist_id>/episodes', endpoint='artist_episodes_api')

# Release
api.add_resource(ReleaseApi, '/api/releases', '/api/releases/<int:release_id>', endpoint='releases_api')
api.add_resource(ReleasesArtistsApi, '/api/releases/<int:release_id>/artists', endpoint='release_artists_api')

# Song
api.add_resource(SongApi, '/api/songs/<string:song_id>', endpoint='songs_api')

import archive.views
