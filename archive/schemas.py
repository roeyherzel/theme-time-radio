from flask import url_for
from marshmallow_jsonapi import Schema, fields
from marshmallow import validate


class TracksTagStatusSchema(Schema):
    id = fields.Integer()
    song = fields.Integer()
    release = fields.Integer()
    artist = fields.Integer()

    class Meta:
        type_ = 'tag_status'


class TracksTagQuerySchema(Schema):
    id = fields.Integer()
    song = fields.Str()
    release = fields.Str()
    artist = fields.Str()

    class Meta:
        type_ = 'tag_query'


class TracksSchema(Schema):
    id = fields.Integer()
    title = fields.Str()
    position = fields.Integer()
    resolved = fields.Boolean()
    episode_id = fields.Integer()
    tags_query = fields.Nested(TracksTagQuerySchema, many=True)
    tags_status = fields.Nested(TracksTagStatusSchema, many=True)

    class Meta:
        type_ = 'track'


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


class ArtistsSchema(Schema):
    id = fields.Integer()
    name = fields.Str()
    thumb = fields.Str()
    profile = fields.Str()
    type = fields.Str()
    real_name = fields.Str()

    class Meta:
        type_ = 'artist'
