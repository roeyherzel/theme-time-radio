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
api.add_resource(Episode, '/api/episodes', '/api/episodes/<int:episode_id>', endpoint='episode_api')
api.add_resource(Tracklist, '/api/episodes/<int:episode_id>/tracklist', endpoint='tracklist_api')

# Artist
api.add_resource(Artist, '/api/artists', '/api/artists/<int:artist_id>', endpoint='artist_api')
api.add_resource(ArtistsReleases, '/api/artists/<int:artist_id>/releases', endpoint='artist_releases_api')
api.add_resource(ArtistsEpisodes, '/api/artists/<int:artist_id>/episodes', endpoint='artist_episodes_api')

# Release
api.add_resource(Release, '/api/releases', '/api/releases/<int:release_id>', endpoint='releases_api')
api.add_resource(ReleasesArtists, '/api/releases/<int:release_id>/artists', endpoint='release_artists_api')

# Song
api.add_resource(Song, '/api/songs/<string:song_id>', endpoint='songs_api')

import archive.views
