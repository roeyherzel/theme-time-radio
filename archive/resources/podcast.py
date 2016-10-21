from archive.models.podcast import Episodes
from archive.common.utils import limit_query
from archive.resources.schemas import EpisodeSchema, EpisodesTracklistSchema

from flask_restful import Resource, reqparse, marshal_with
from sqlalchemy import desc


class EpisodesAPI(Resource):

    @marshal_with(EpisodeSchema)
    def get(self, episode_id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('limit', type=int, help="limit query results")
        args = parser.parse_args()

        if episode_id is not None:
            return Episodes.query.get(episode_id)
        else:
            return limit_query(Episodes.query.order_by(Episodes.id), args.get('limit')).all()


class EpisodesTracklistAPI(Resource):

    @marshal_with(EpisodesTracklistSchema)
    def get(self, episode_id):
        return Episodes.query.get(episode_id)
