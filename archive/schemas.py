from marshmallow_jsonapi import Schema, fields
from marshmallow import validate


class EpisodesSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')
    id = fields.Integer(dump_only=True)
    title = fields.Str()
    plot = fields.Str()
    description = fields.Str()
    guest = fields.Str()
    date_pub = fields.Date()
    date_add = fields.Date()
    podcast_url = fields.Url()
    thumb = fields.Str()

    class Meta:
        type_ = 'episode'


class TracksSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')
    id = fields.Integer(dump_only=True)
    title = fields.Str()
    position = fields.Integer()
    episode_id = fields.Integer()

    class Meta:
        type_ = 'track'


class ArtistsSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')
    id = fields.Integer(dump_only=True)
    name = fields.Str()
    thumb = fields.Str()
    profile = fields.Str()
    type = fields.Str()
    real_name = fields.Str()

    class Meta:
        type_ = 'artist'
