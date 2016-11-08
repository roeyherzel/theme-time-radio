from archive.models import podcast
from archive.common.utils import limit_query
from archive.resources import schemas

from flask_restful import Resource, reqparse, marshal_with, abort
from sqlalchemy import desc

from archive import api


@api.resource('/api/episodes', '/api/episodes/<int:episode_id>')
class EpisodesAPI(Resource):

    @marshal_with(schemas.Episode().as_dict)
    def get(self, episode_id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('limit', type=int, help="limit query results")
        args = parser.parse_args()

        if episode_id is not None:
            return podcast.Episodes.query.get(episode_id)
        else:
            return limit_query(podcast.Episodes.query.order_by(podcast.Episodes.id), args.get('limit')).all()


@api.resource('/api/episodes/<int:episode_id>/tracklist')
class EpisodesTracklistAPI(Resource):

    @marshal_with(schemas.Track().as_dict)
    def get(self, episode_id):
        episode = podcast.Episodes.query.get(episode_id)
        if episode is None:
            abort(404)

        return episode.tracklist.all()
