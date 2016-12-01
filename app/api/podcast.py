from flask_restful import Resource, reqparse, marshal_with, abort
from . import api
from . import schemas
from ..models import Episodes, Tracks


@api.resource('/api/episodes', '/api/episodes/<int:episode_id>')
class EpisodesAPI(Resource):

    @marshal_with(schemas.Episode().as_dict)
    def get(self, episode_id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('limit', type=int, help="limit query results")
        args = parser.parse_args()

        if episode_id:
            return Episodes.query.get(episode_id)

        res = Episodes.query.order_by(Episodes.id)
        if args.get('limit'):
            res = res.limit(args.get('limit'))

        return res.all()


@api.resource('/api/episodes/<int:episode_id>/tracklist')
class EpisodesTracklistAPI(Resource):

    @marshal_with(schemas.Track().as_dict)
    def get(self, episode_id):
        episode = Episodes.query.get(episode_id)
        if episode is None:
            abort(404)

        return episode.tracklist.order_by(Tracks.position).all()
