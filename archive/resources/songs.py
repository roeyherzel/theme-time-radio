from archive.models import *
from archive.schemas import SongsSchema

from flask_restful import Resource
from flask import jsonify


class Song(Resource):

    def get(self, song_id):
        song = Songs.query.get(song_id)
        res = SongsSchema().dump(song)
        return jsonify(res.data['data'])
