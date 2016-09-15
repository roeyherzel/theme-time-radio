from flask import url_for
from marshmallow_jsonapi import Schema, fields
from marshmallow import validate
from archive.models import *


class TracksTagStatusSchema(Schema):
    id = fields.Integer()
    song = fields.Function(lambda obj: Status.getNameById(obj.song))
    release = fields.Function(lambda obj: Status.getNameById(obj.release))
    artist = fields.Function(lambda obj: Status.getNameById(obj.artist))
    aggregated = fields.Function(lambda obj: Status.getNameById(obj.aggregated))

    class Meta:
        type_ = 'tag_status'


class TracksTagQuerySchema(Schema):
    id = fields.Integer()
    song = fields.Str()
    release = fields.Str()
    artist = fields.Str()

    class Meta:
        type_ = 'tag_query'


class ArtistsImages(Schema):
    id = fields.Integer()
    type = fields.Str()
    width = fields.Integer()
    height = fields.Integer()
    uri = fields.Url()
    uri150 = fields.Url()

    class Meta:
        type_ = 'image'


class ArtistsGroups(Schema):
    id = fields.Integer()
    name = fields.Str()

    class Meta:
        type_ = 'group'


class ArtistsMembers(Schema):
    id = fields.Integer()
    name = fields.Str()

    class Meta:
        type_ = 'member'


class ArtistsAliases(Schema):
    id = fields.Integer()
    name = fields.Str()

    class Meta:
        type_ = 'alias'


class ArtistsUrls(Schema):
    id = fields.Integer()
    url = fields.Url()

    class Meta:
        type_ = 'artist_url'


class ArtistsSchema(Schema):
    id = fields.Integer()
    name = fields.Str()
    thumb = fields.Str()
    profile = fields.Str()
    type = fields.Str()
    real_name = fields.Str()
    images = fields.Nested(ArtistsImages, many=True)
    groups = fields.Nested(ArtistsGroups, many=True)
    members = fields.Nested(ArtistsMembers, many=True)
    aliases = fields.Nested(ArtistsAliases, many=True)
    urls = fields.Nested(ArtistsUrls, many=True)

    class Meta:
        type_ = 'artist'
        self_url = 'artists/{artist_id}'
        self_url_kwargs = {'artist_id': '<id>'}


class ReleasesSchema(Schema):
    id = fields.Integer()
    title = fields.Str()
    thumb = fields.Str()
    year = fields.Integer()

    class Meta:
        type_ = 'release'
        self_url = 'releases/{release_id}'
        self_url_kwargs = {'release_id': '<id>'}


class SongsSchema(Schema):
    id = fields.Str()
    title = fields.Str()

    class Meta:
        type_ = 'song'
        self_url = 'songs/{song_id}'
        self_url_kwargs = {'song_id': '<id>'}


class TracksArtistsSchema(Schema):
    id = fields.Integer()
    artist_id = fields.Integer()

    class Meta:
        type_ = 'artists'
        self_url = 'artists/{artist_id}'
        self_url_kwargs = {'artist_id': '<artist_id>'}


class TracksReleasesSchema(Schema):
    id = fields.Integer()
    release_id = fields.Integer()

    class Meta:
        type_ = 'releases'
        self_url = 'releases/{release_id}'
        self_url_kwargs = {'release_id': '<release_id>'}


class TracksSongsSchema(Schema):
    id = fields.Integer()
    song_id = fields.Str()

    class Meta:
        type_ = 'songs'
        self_url = 'songs/{song_id}'
        self_url_kwargs = {'song_id': '<song_id>'}


class TracksSchema(Schema):
    id = fields.Integer()
    title = fields.Str()
    position = fields.Integer()
    resolved = fields.Boolean()
    episode_id = fields.Integer()
    tags_query = fields.Nested(TracksTagQuerySchema, many=True)
    tags_status = fields.Nested(TracksTagStatusSchema, many=True)

    song_tags = fields.Nested(TracksSongsSchema, many=True)
    release_tags = fields.Nested(TracksReleasesSchema, many=True)
    artist_tags = fields.Nested(TracksArtistsSchema, many=True)

    class Meta:
        type_ = 'track'


class EpisodesCategoriesSchema(Schema):
    id = fields.Integer()
    category = fields.Str()

    class Meta:
        type_ = 'category'


class EpisodesSchema(Schema):
    id = fields.Integer()
    title = fields.Str()
    plot = fields.Str()
    description = fields.Str()
    guest = fields.Str()
    date_pub = fields.Date()
    date_add = fields.Date()
    podcast_url = fields.Url()
    thumb = fields.Str()
    categories = fields.Nested(EpisodesCategoriesSchema, many=True)

    class Meta:
        type_ = 'episodes'
        self_url = 'episodes/{id}'
        self_url_kwargs = {'id': '<id>'}
        self_url_many = 'episodes/'
        strict = True


class EpisodesTracklistScheam(Schema):
    id = fields.Integer()
    tracklist = fields.Nested(TracksSchema, many=True)

    class Meta:
        type_ = 'playlist'
        strict = True
