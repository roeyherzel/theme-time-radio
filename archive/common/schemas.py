from flask_restful import fields
from flask import url_for


ImageSchema = {
    'id': fields.Integer,
    'type': fields.String,
    'uri': fields.String,
}

SongSchema = {
    'resource_path': fields.FormattedString("songs/{id}"),
    'id': fields.String,
    'title': fields.String,
    'position': fields.String,
    'type': fields.String,
    'duration': fields.String,
    'album_path': fields.FormattedString("albums/{album_id}"),
    'tracks': fields.List(fields.Nested({'track_id': fields.Integer})),
    'album': fields.Nested(
        {
            'resource_path': fields.FormattedString("albums/{id}"),
            'id': fields.Integer,
            'title': fields.String,
            'thumb': fields.String,
            'year': fields.Integer,
            'images': fields.List(fields.Nested(ImageSchema)),
        })
}


ArtistSchema = {
    'resource_path': fields.FormattedString("artists/{id}"),
    'id': fields.Integer,
    'name': fields.String,
    'thumb': fields.String,
    'profile': fields.String,
    'type': fields.String,
    'real_name': fields.String,
    'images': fields.List(fields.Nested(ImageSchema)),
    'groups': fields.List(fields.Nested({'name': fields.String})),
    'members': fields.List(fields.Nested({'name': fields.String})),
    'aliases': fields.List(fields.Nested({'name': fields.String})),
    'urls': fields.List(fields.Nested({'url': fields.String})),
}


AlbumsArtistsSchema = {
    'artist_id': fields.Integer,
    'resource_path': fields.FormattedString("artists/{artist_id}"),
}


AlbumSchema = {
    'resource_path': fields.FormattedString("albums/{id}"),
    'id': fields.Integer,
    'title': fields.String,
    'thumb': fields.String,
    'year': fields.Integer,
    'genres': fields.List(fields.Nested({'genre': fields.String})),
    'styles': fields.List(fields.Nested({'style': fields.String})),
    'images': fields.List(fields.Nested(ImageSchema)),
    'songs': fields.List(fields.Nested(SongSchema)),
    'artists': fields.List(fields.Nested(AlbumsArtistsSchema))
}


TrackTagStatusSchema = {
}

TrackTagQuerySchema = {
    'song': fields.String,
    'album': fields.String,
    'artist': fields.String,
}

TrackSongsSchema = {
    'song_id': fields.String,
    'resource_path': fields.FormattedString("songs/{song_id}"),
}
TrackAlbumSchema = {
    'album_id': fields.Integer,
    'resource_path': fields.FormattedString("albums/{album_id}"),
}
TrackArtistSchema = {
    'artist_id': fields.Integer,
    'resource_path': fields.FormattedString("artists/{artist_id}"),
}
