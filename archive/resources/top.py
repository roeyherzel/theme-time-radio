from archive.models import *
from archive.common.utils import limit_query

from flask_restful import Resource, marshal_with, reqparse, fields
from sqlalchemy import desc, func

from archive.common.schemas import ArtistSchema, AlbumSchema, SongSchema

TopArtistSchema = {
    'artist': fields.Nested(ArtistSchema),
    'play_count': fields.Integer
}

TopAlbumSchema = {
    'album': fields.Nested(AlbumSchema),
    'play_count': fields.Integer
}

TopSongSchema = {
    'song': fields.Nested(SongSchema),
    'play_count': fields.Integer
}


class ApiTopArtists(Resource):

    @marshal_with(TopArtistSchema)
    def get(self, artist_id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('limit', type=int, help="limit query results")
        args = parser.parse_args()

        myQuery = db.session.query(Artists, func.count(Artists.id).label('play_count')) \
                            .join(TracksArtists, (Artists.id == TracksArtists.artist_id)) \
                            .filter(TracksArtists.status == Status.getIdByName('matched')) \
                            .group_by(Artists.id) \
                            .order_by(func.count(Artists.id).desc())

        myQuery = limit_query(myQuery, args.get('limit')).all()
        myQuery = [dict({'artist': i[0], 'play_count': i[1]}) for i in myQuery]
        return myQuery


class ApiTopSongs(Resource):

    @marshal_with(TopSongSchema)
    def get(self, song_id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('limit', type=int, help="limit query results")
        args = parser.parse_args()

        myQuery = db.session.query(Songs, func.count(Songs.id).label('play_count')) \
                            .join(TracksSongs, (Songs.id == TracksSongs.song_id)) \
                            .filter(TracksSongs.status == Status.getIdByName('matched')) \
                            .group_by(Songs.id) \
                            .order_by(func.count(Songs.id).desc())

        myQuery = limit_query(myQuery, args.get('limit')).all()
        myQuery = [dict({'song': i[0], 'play_count': i[1]}) for i in myQuery]
        return myQuery
