
from archive.models import spotify, podcast
from archive.common.utils import limit_query
from archive.resources import schemas

from flask_restful import Resource, reqparse, marshal, marshal_with, marshal_with_field, fields
from sqlalchemy import desc

from archive import api


parser = reqparse.RequestParser()
parser.add_argument('limit', type=str, help="limit query results")


@api.resource('/api/artists', '/api/artists/<string:artist_id>')
class ArtistsAPI(Resource):

    @marshal_with(schemas.Artist().as_dict)
    def get(self, artist_id=None):
        args = parser.parse_args()

        if artist_id is not None:
            return spotify.Artists.query.get(artist_id)
        else:
            return limit_query(spotify.Artists.query.order_by(spotify.Artists.name), args.get('limit')).all()


@api.resource('/api/artists/<string:artist_id>/tracklist')
class ArtistsTracklistAPI(Resource):

    @marshal_with(schemas.ArtistTracklist().as_dict)
    def get(self, artist_id):
        res = podcast.Tracks.query.join(spotify.TracksArtists, (podcast.Tracks.id == spotify.TracksArtists.track_id)) \
                                  .filter(spotify.TracksArtists.artist_id == artist_id) \
                                  .all()
        return {'tracklist': res}


@api.resource('/api/tags')
class TagsAPI(Resource):
    parser.add_argument('artist_id', type=str, help="artists tags")

    def get(self, artist_id=None):
        args = parser.parse_args()
        artist_id = args.get('artist_id')

        if artist_id is not None:
            return marshal(spotify.Artists.query.get(artist_id), schemas.ArtistTags().as_dict)

        return marshal(spotify.Tags.query.all(), schemas.Tags().as_dict)


# TODO: move this to ArtistsAPI with request parameter
@api.resource('/api/lastfm/artists')
class LastFmArtistsAPI(Resource):

    @marshal_with_field(fields.List(fields.String()))
    def get(self):
        # NOTE: used to wraped/envelope with data:
        return [i.lastfm_name for i in spotify.Artists.query.all()]
