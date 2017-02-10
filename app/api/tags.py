from flask_restful import Resource, reqparse, marshal_with, abort
from . import api
from . import schemas
from ..models import *
from sqlalchemy import desc, func

parser = reqparse.RequestParser()
parser.add_argument('limit', type=str, help="limit query results")
parser.add_argument('random', type=str, help="limit query results")


@api.resource('/api/tags', '/api/tags/<string:tag_name>')
class TagsAPI(Resource):

    @marshal_with(schemas.TagsCount().as_dict)
    def get(self, tag_name=None):
        return tag_name
        # res = Tags.countSong()
        #
        # if tag_name:
        #     res = res.filter(Tags.name == tag_name).first()
        #     return {'tag': res[0], 'track_count': res[1]}
        #
        # args = parser.parse_args()
        # if args.get('random'):
        #     res = res.order_by(func.random())
        # else:
        #     res = res.order_by(desc('track_count'))
        #
        # if args.get('limit'):
        #     res = res.limit(args.get('limit'))
        #
        # return [{'tag': i.Tags, 'track_count': i.track_count} for i in res.all()]


@api.resource('/api/tags/<string:tag_name>/artists')
class TagsArtistsAPI(Resource):

    @marshal_with(schemas.Artist().as_dict)
    def get(self, tag_name):
        return Artists.query.join(aux_songs_artists, aux_songs_artists.c.artist_id == Artists.id) \
                            .join(aux_songs_tags, aux_songs_tags.c.song_id == aux_songs_artists.c.song_id) \
                            .filter(aux_songs_tags.c.tag_id == Tags.getId(tag_name)) \
                            .all()


@api.resource('/api/tags/<string:tag_name>/songs')
class TagsSongsAPI(Resource):

    @marshal_with(schemas.Song().as_dict)
    def get(self, tag_name):
        return Tags.query.get(Tags.getId(tag_name)).songs
