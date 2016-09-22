from archive.models import *
from archive.common.schemas import SongSchema, ArtistSchema
from flask_restful import Resource, marshal_with


class SongApi(Resource):

    @marshal_with(SongSchema)
    def get(self, song_id):
        return Songs.query.get(song_id)
