from archive.models.podcast import Episodes
from archive.common.utils import limit_query

from flask import url_for
from flask_restful import Resource, reqparse, marshal_with, fields
from sqlalchemy import desc


class UrlField(fields.Raw):
    def output(self, key, obj):
        return url_for(self.attribute, episode_id=obj.id, _external=True)

SpotifyDataSchema = {
    'song_data': fields.Nested({
        'id': fields.String,
        'name': fields.String,
    }),
    'artist_id': fields.String
}

SpotifyResouceSchema = {
    'id': fields.String,
    'name': fields.String,
}

TrackSchema = {
    'id': fields.Integer,
    'resolved': fields.Boolean,
    'title': fields.String,
    'parsed_song': fields.String,
    'parsed_artist': fields.String,
    'position': fields.Integer,
    'tags': fields.List(fields.Nested({'tag': fields.String})),
    'spotify_song': fields.Nested(SpotifyResouceSchema)
}

EpisodeSchema = {
    'view_url': UrlField(attribute="episodes_info"),
    'api_url': UrlField(attribute="episodes_api"),
    'id': fields.Integer,
    'title': fields.String,
    'tags': fields.List(fields.Nested({'tag': fields.String})),
}

EpisodesTracklistSchema = {
    'tracklist': fields.List(fields.Nested(TrackSchema))
}


class EpisodesAPI(Resource):

    @marshal_with(EpisodeSchema)
    def get(self, episode_id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('limit', type=int, help="limit query results")
        args = parser.parse_args()

        if episode_id is not None:
            return Episodes.query.get(episode_id)
        else:
            return limit_query(Episodes.query.order_by(desc(Episodes.date_pub)), args.get('limit')).all()


class EpisodesTracklistAPI(Resource):

    @marshal_with(EpisodesTracklistSchema)
    def get(self, episode_id):
        return Episodes.query.get(episode_id)
