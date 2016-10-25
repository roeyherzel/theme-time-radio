from flask import url_for
from flask_restful import fields


SpotifyResourceSchema = {
    'id': fields.String,
    'name': fields.String,
    'url': fields.String,
    'preview_url': fields.String,
    'image': fields.String
}

EpisodeSchema = {
    'id': fields.Integer,
    'view': fields.FormattedString("episodes/{id}"),
    'api': fields.FormattedString("api/episodes/{id}"),
    'title': fields.String,
    'season': fields.Integer,
    'image': fields.String,
    'tags': fields.List(fields.Nested({'tag': fields.String})),
}

TrackSchema = {
    'id': fields.Integer,
    'resolved': fields.Boolean,
    'title': fields.String,
    'parsed_song': fields.String,
    'parsed_artist': fields.String,
    'position': fields.Integer,
    'year': fields.Integer,
    'spotify_song': fields.Nested({'song': fields.Nested(SpotifyResourceSchema)}),
    'spotify_album': fields.Nested({'album': fields.Nested(SpotifyResourceSchema)}),
    'spotify_artist': fields.Nested({'artist': fields.Nested(SpotifyResourceSchema)}),
}


PlaylistTrackSchema = {
    'episode': fields.Nested(EpisodeSchema)
}
PlaylistTrackSchema.update(TrackSchema)


TracklistSchema = {
    'tracklist': fields.List(fields.Nested(TrackSchema))
}

PlaylistSchema = {
    'tracklist': fields.List(fields.Nested(PlaylistTrackSchema))
}
