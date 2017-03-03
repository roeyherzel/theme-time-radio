from flask_restful import Resource, reqparse, marshal_with, marshal_with_field, fields, abort
from . import api
from . import schemas
from ..models import *
from sqlalchemy import func

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
            # filter only artists with images
            res = res.filter(Artists.lastfm_image != None, Artists.lastfm_image != '').limit(args.get('limit'))

        return res.all()


@api.resource('/api/artists/<string:artist_id>/episodes')
class ArtistsEpisodesAPI(Resource):

    @marshal_with(schemas.Episode().as_dict)
    def get(self, artist_id):
        return Episodes.query.join(Tracks, Tracks.episode_id == Episodes.id) \
                             .join(aux_tracks_artists, aux_tracks_artists.c.track_id == Tracks.id) \
                             .filter(aux_tracks_artists.c.artist_id == artist_id) \
                             .order_by(Tracks.episode_id, Tracks.position) \
                             .all()


@api.resource('/api/artists/<string:artist_id>/tracklist')
class ArtistsTracklistAPI(Resource):

    @marshal_with(schemas.Track().as_dict)
    def get(self, artist_id):
        return Artists.query.get(artist_id).tracks


@api.resource('/api/helper/all-lastfm-artists')
class LastFmArtistsAPI(Resource):

    @marshal_with_field(fields.List(fields.String()))
    def get(self):
        return [i.lastfm_name for i in Artists.query.all()]
