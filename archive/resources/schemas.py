from flask import url_for
from flask_restful import fields


SpotifyResourceSchema = {
    'id': fields.String,
    'name': fields.String,
    'url': fields.String,
}

SpotifySongSchema = {
    'album': fields.Nested(SpotifyResourceSchema),
    'preview_url': fields.String,
}
SpotifyArtistSchema = {
    'view': fields.FormattedString("artists/{id}"),
    'lastfm_name': fields.String,
    'lastfm_image': fields.String,
}

SpotifyArtistSchema.update(SpotifyResourceSchema)
SpotifySongSchema.update(SpotifyResourceSchema)


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
    'spotify_song': fields.Nested({'data': fields.Nested(SpotifySongSchema)}),
    'spotify_artists': fields.Nested({'data': fields.Nested(SpotifyArtistSchema)}),
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
