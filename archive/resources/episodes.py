from archive.common.utils import limit_api_results
from archive.common.schemas import EpisodeSchema, EpisodeTracklistScheam
from archive.models import *

from flask_restful import Resource, reqparse, marshal_with

from sqlalchemy import desc


class EpisodeApi(Resource):

    @marshal_with(EpisodeSchema)
    def get(self, episode_id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('limit', type=int, help="limit query results")
        args = parser.parse_args()
        print(args)

        if episode_id is not None:
            return Episodes.query.get(episode_id)
        else:
            return limit_api_results(Episodes.query.order_by(desc(Episodes.date_pub)), args.get('limit')).all()


class TracklistApi(Resource):

    @marshal_with(EpisodeTracklistScheam)
    def get(self, episode_id):
        return Episodes.query.get(episode_id)
