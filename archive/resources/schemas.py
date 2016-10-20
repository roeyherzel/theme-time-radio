from flask import url_for
from flask_restful import fields


class UrlField(fields.Raw):
    def output(self, key, obj):
        return url_for(self.attribute, episode_id=obj.id, _external=True)


SpotifyResourceSchema = {
    'id': fields.String,
    'name': fields.String,
    'url': fields.String,
}

EpisodeSchema = {
    'view_url': UrlField(attribute="episodes_info"),
    'api_url': UrlField(attribute="episodes_api"),
    'id': fields.Integer,
    'title': fields.String,
    'tags': fields.List(fields.Nested({'tag': fields.String})),
}

TrackSchema = {
    'id': fields.Integer,
    'resolved': fields.Boolean,
    'title': fields.String,
    'parsed_song': fields.String,
    'parsed_artist': fields.String,
    'position': fields.Integer,
    'tags': fields.List(fields.Nested({'tag': fields.String})),
    'spotify_song': fields.Nested({'song': fields.Nested(SpotifyResourceSchema)}),
    'spotify_album': fields.Nested({'album': fields.Nested(SpotifyResourceSchema)}),
    'spotify_artist': fields.Nested({'artist': fields.Nested(SpotifyResourceSchema)}),
}


EpisodesTracklistSchema = {
    'tracklist': fields.List(fields.Nested(TrackSchema))
}
