from archive.common import utils
from archive.models import *
from archive.schemas import EpisodesSchema, EpisodesTracklistScheam

from flask_restful import Resource, reqparse
from flask import jsonify


class Episode(Resource):
    def get(self, episode_id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('limit', type=int, help="limit query results")
        args = parser.parse_args()
        print(args)

        if episode_id is not None:
            ep = Episodes.query.get(episode_id)
            res = EpisodesSchema().dump(ep)
        else:
            ep = utils.limit_api_results(Episodes.query.order_by(Episodes.date_pub), args.get('limit'))
            res = EpisodesSchema().dump(ep.all(), many=True)

        return jsonify(res.data['data'])


class Tracklist(Resource):
    def get(self, episode_id):
        ep = Episodes.query.get(episode_id)
        res = EpisodesTracklistScheam().dump(ep)
        return jsonify(res.data['data']['attributes']['tracklist']['data'])
