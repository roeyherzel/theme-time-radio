from flask_restful import Resource, reqparse, marshal_with, abort
from . import api
from . import schemas
from ..models import *
from sqlalchemy import desc, func

parser = reqparse.RequestParser()
parser.add_argument('limit', type=str, help="limit query results")
parser.add_argument('random', type=str, help="limit query results")


@api.resource('/api/genres', '/api/genres/<string:tag_name>')
class TagsAPI(Resource):

    @marshal_with(schemas.Tags().as_dict)
    def get(self, tag_name=None):
        if tag_name is None:
            # TODO: filter only tags that has > songs
            return Tags.query.order_by(Tags.name).all()
        else:
            return Tags.query.filter(Tags.name == tag_name).first()


@api.resource('/api/genres/<string:tag>/artists')
class TagsArtistsAPI(Resource):

    @marshal_with(schemas.Artist().as_dict)
    def get(self, tag):
        return Artists.query.join(aux_artists_tags, aux_artists_tags.c.artist_id == Artists.id) \
                            .filter(aux_artists_tags.c.tag_id == Tags.getId(tag)) \
                            .all()


@api.resource('/api/genres/<string:tag>/tracklist')
class TagsTracklistAPI(Resource):

    @marshal_with(schemas.Track().as_dict)
    def get(self, tag):
        return Tracks.query.join(aux_tracks_artists, aux_tracks_artists.c.track_id == Tracks.id) \
                           .join(aux_artists_tags, aux_artists_tags.c.artist_id == aux_tracks_artists.c.artist_id) \
                           .filter(aux_artists_tags.c.tag_id == Tags.getId(tag)) \
                           .order_by(Tracks.episode_id, Tracks.position) \
                           .all()
