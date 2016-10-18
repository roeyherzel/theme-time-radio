from flask import Flask
from flask_restful import Api
from archive.resources.episodes import *
from archive.resources.tracks import *
from archive.resources.artists import *
from archive.resources.songs import *
from archive.resources.top import *

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
api.add_resource(ApiTracksArtists, '/api/tracks/<int:track_id>/match/artist', endpoint='tracks_artists_api')
api.add_resource(ApiTracksSongs, '/api/tracks/<int:track_id>/match/song', endpoint='tracks_songs_api')

# Artist
api.add_resource(ApiArtist, '/api/artists', '/api/artists/<int:artist_id>', endpoint='artist_api')
api.add_resource(ApiArtistsSongs, '/api/artists/<int:artist_id>/songs', endpoint='artist_songs_api')
api.add_resource(ApiArtistsEpisodes, '/api/artists/<int:artist_id>/episodes', endpoint='artist_episodes_api')
api.add_resource(ApiTopArtists, '/api/artists/top', endpoint='top_artists_api')

# Song
api.add_resource(ApiSong, '/api/songs/<string:song_id>', endpoint='songs_api')
api.add_resource(ApiSongsEpisodes, '/api/songs/<string:song_id>/episodes', endpoint='songs_episodes_api')
api.add_resource(ApiTopSongs, '/api/songs/top', endpoint='top_songs_api')


import archive.views
