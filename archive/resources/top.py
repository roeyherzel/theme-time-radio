from archive.models import *
from archive.common.utils import limit_query

from flask_restful import Resource, marshal_with, reqparse, fields
from sqlalchemy import desc, func


TopArtistSchema = {
    'artist_id': fields.Integer,
    'artist_path': fields.FormattedString("artists/{artist_id}"),
    'play_count': fields.Integer
}

TopReleaseSchema = {
    'release_id': fields.Integer,
    'release_path': fields.FormattedString("releases/{release_id}"),
    'play_count': fields.Integer
}

TopSongSchema = {
    'song_id': fields.String,
    'song_path': fields.FormattedString("songs/{song_id}"),
    'play_count': fields.Integer
}


class ApiTopArtists(Resource):

    @marshal_with(TopArtistSchema)
    def get(self, artist_id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('limit', type=int, help="limit query results")
        args = parser.parse_args()

        myQuery = db.session.query(TracksArtists.artist_id.label('artist_id'),
                                   func.count(TracksArtists.track_id).label('play_count')) \
                            .filter(TracksArtists.status == Status.getIdByName('matched')) \
                            .group_by(TracksArtists.artist_id) \
                            .order_by(func.count(TracksArtists.track_id).desc())

        myQuery = limit_query(myQuery, args.get('limit')).all()
        myQuery = [dict({'artist_id': i.artist_id, 'play_count': i.play_count}) for i in myQuery]
        return myQuery


class ApiTopReleases(Resource):

    @marshal_with(TopReleaseSchema)
    def get(self, release_id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('limit', type=int, help="limit query results")
        args = parser.parse_args()

        myQuery = db.session.query(TracksReleases.release_id.label('release_id'),
                                   func.count(TracksReleases.track_id).label('play_count')) \
                            .filter(TracksReleases.status == Status.getIdByName('matched')) \
                            .group_by(TracksReleases.release_id) \
                            .order_by(func.count(TracksReleases.track_id).desc())

        myQuery = limit_query(myQuery, args.get('limit')).all()
        myQuery = [dict({'release_id': i.release_id, 'play_count': i.play_count}) for i in myQuery]
        return myQuery


class ApiTopSongs(Resource):

    @marshal_with(TopSongSchema)
    def get(self, song_id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('limit', type=int, help="limit query results")
        args = parser.parse_args()

        myQuery = db.session.query(TracksSongs.song_id.label('song_id'),
                                   func.count(TracksSongs.track_id).label('play_count')) \
                            .filter(TracksSongs.status == Status.getIdByName('matched')) \
                            .group_by(TracksSongs.song_id) \
                            .order_by(func.count(TracksSongs.track_id).desc())

        myQuery = limit_query(myQuery, args.get('limit')).all()
        myQuery = [dict({'song_id': i.song_id, 'play_count': i.play_count}) for i in myQuery]
        return myQuery
