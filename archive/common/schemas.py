from flask_restful import fields
from flask import url_for

from archive.models import Status


class get_status_name(fields.Raw):
    def output(self, key, obj):
        return Status.getNameById(getattr(obj, key))


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
    'release_path': fields.FormattedString("releases/{release_id}"),
    'tracks': fields.List(fields.Nested({'track_id': fields.Integer})),
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


ReleasesArtistsSchema = {
    'artist_id': fields.Integer,
    'resource_path': fields.FormattedString("artists/{artist_id}"),
}


ReleaseSchema = {
    'resource_path': fields.FormattedString("releases/{id}"),
    'id': fields.Integer,
    'title': fields.String,
    'thumb': fields.String,
    'year': fields.Integer,
    'genres': fields.List(fields.Nested({'genre': fields.String})),
    'styles': fields.List(fields.Nested({'style': fields.String})),
    'images': fields.List(fields.Nested(ImageSchema)),
    'songs': fields.List(fields.Nested(SongSchema)),
    'artists': fields.List(fields.Nested(ReleasesArtistsSchema))
}


TrackTagStatusSchema = {
    'song': get_status_name,
    'release': get_status_name,
    'artist': get_status_name,
    'aggregated': get_status_name,
}

TrackTagQuerySchema = {
    'song': fields.String,
    'release': fields.String,
    'artist': fields.String,
}

TrackSongsSchema = {
    'song_id': fields.String,
    'resource_path': fields.FormattedString("songs/{song_id}"),
}
TrackReleaseSchema = {
    'release_id': fields.Integer,
    'resource_path': fields.FormattedString("releases/{release_id}"),
}
TrackArtistSchema = {
    'artist_id': fields.Integer,
    'resource_path': fields.FormattedString("artists/{artist_id}"),
}

TrackSchema = {
    'id': fields.Integer,
    'title': fields.String,
    'position': fields.Integer,
    'resolved': fields.Boolean,
    'episode_id': fields.Integer,
    'tags_query': fields.List(fields.Nested(TrackTagQuerySchema)),
    'tags_status': fields.List(fields.Nested(TrackTagStatusSchema)),  # NOTE: need to remove the list, but make it work

    'tags_song': fields.List(fields.Nested(TrackSongsSchema)),
    'tags_release': fields.List(fields.Nested(TrackReleaseSchema)),
    'tags_artist': fields.List(fields.Nested(TrackArtistSchema)),
}


EpisodeSchema = {
    'resource_path': fields.FormattedString("episodes/{id}"),
    'id': fields.Integer,
    'title': fields.String,
    'plot': fields.String,
    'description': fields.String,
    'guest': fields.String,
    'date_pub': fields.DateTime,
    'date_add': fields.DateTime,
    'podcast_url': fields.String,
    'thumb': fields.String,
    'categories': fields.List(fields.Nested({'category': fields.String})),
}


EpisodeTracklistScheam = {
    'tracklist': fields.List(fields.Nested(TrackSchema))
}
