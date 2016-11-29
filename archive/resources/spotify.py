from archive.models import db
from archive.models.models import *
from archive.resources import schemas

from flask_restful import Resource, reqparse, marshal, marshal_with, marshal_with_field, fields
from sqlalchemy import desc, distinct, func

from archive import api


parser = reqparse.RequestParser()
parser.add_argument('limit', type=str, help="limit query results")
parser.add_argument('random', type=str, help="limit query results")


@api.resource('/api/artists', '/api/artists/<string:artist_id>')
class ArtistsAPI(Resource):

    @marshal_with(schemas.Artist().as_dict)
    def get(self, artist_id=None):
        args = parser.parse_args()

        if artist_id:
            return Artists.query.get(artist_id)

        order = func.random() if args.get('random') else Artists.name
        res = Artists.query.order_by(order)

        if args.get('limit'):
            # filter only artists that have images
            res = res.filter(Artists.lastfm_image != None, Artists.lastfm_image != '').limit(args.get('limit'))

        return res.all()


@api.resource('/api/artists/<string:artist_id>/episodes')
class ArtistsEpisodesAPI(Resource):

    @marshal_with(schemas.Episode().as_dict)
    def get(self, artist_id):
        return Episodes.query.join(Tracks, Tracks.episode_id == Episodes.id) \
                             .join(association_track_artists, association_track_artists.c.track_id == Tracks.id) \
                             .filter(association_track_artists.c.artist_id == artist_id) \
                             .all()


@api.resource('/api/artists/<string:artist_id>/tracklist')
class ArtistsTracklistAPI(Resource):

    @marshal_with(schemas.ArtistTracklist().as_dict)
    def get(self, artist_id):
        res = Tracks.query.join(association_track_artists, (Tracks.id == association_track_artists.c.track_id)) \
                          .filter(association_track_artists.c.artist_id == artist_id) \
                          .all()
        return {'tracklist': res}


@api.resource('/api/artists/<string:artist_id>/tags')
class ArtistsTagsAPI(Resource):

    @marshal_with(schemas.Tags().as_dict)
    def get(self, artist_id):
        return Artists.query.get(artist_id).tags

"""
-----------------------------
LastFM API
-----------------------------
"""


# TODO: move this to ArtistsAPI with request parameter
@api.resource('/api/lastfm/artists')
class LastFmArtistsAPI(Resource):

    @marshal_with_field(fields.List(fields.String()))
    def get(self):
        # NOTE: used to wraped/envelope with data:
        return [i.lastfm_name for i in Artists.query.all()]
