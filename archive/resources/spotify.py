from archive.models.spotify import SpotifyArtists, TracksSpotifyData
from archive.models.podcast import Tracks
from archive.common.utils import limit_query
from archive.resources.schemas import SpotifyResourceSchema, TracklistSchema

from flask_restful import Resource, reqparse, marshal_with
from sqlalchemy import desc


class ArtistsAPI(Resource):

    @marshal_with(SpotifyResourceSchema)
    def get(self, artist_id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('limit', type=str, help="limit query results")
        args = parser.parse_args()

        if artist_id is not None:
            return SpotifyArtists.query.get(artist_id)
        else:
            return limit_query(SpotifyArtists.query.order_by(SpotifyArtists.name), args.get('limit')).all()


class ArtistsTracksAPI(Resource):

    @marshal_with(TracklistSchema)
    def get(self, artist_id):
        tracks = Tracks.query.join(TracksSpotifyData, (Tracks.id == TracksSpotifyData.track_id)) \
                       .filter(TracksSpotifyData.artist_id == artist_id) \
                       .all()

        return {'tracklist': tracks}
