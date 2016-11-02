
from archive.models import spotify, podcast
from archive.common.utils import limit_query
from archive.resources import schemas

from flask_restful import Resource, reqparse, marshal, marshal_with, marshal_with_field, fields
from sqlalchemy import desc

from archive import api


parser = reqparse.RequestParser()
parser.add_argument('limit', type=str, help="limit query results")

"""
-----------------------------
Artist API
-----------------------------
"""


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


@api.resource('/api/artists/<string:artist_id>/tags')
class ArtistsTagsAPI(Resource):

    @marshal_with(schemas.ArtistTags().as_dict)
    def get(self, artist_id):
        return spotify.Artists.query.get(artist_id)


"""
-----------------------------
Tags/Mixtapes API
-----------------------------
"""


@api.resource('/api/tags')
class TagsAPI(Resource):

    @marshal_with(schemas.Tags().as_dict)
    def get(self):
        return spotify.Tags.query.all()


@api.resource('/api/tags/<string:tag_name>/tracklist')
class TagsSongsAPI(Resource):

    @marshal_with(schemas.ArtistTracklist().as_dict)
    def get(self, tag_name):
        res = podcast.Tracks.query.join(spotify.TracksArtists, (spotify.TracksArtists.track_id == podcast.Tracks.id)) \
                                  .join(spotify.Artists, (spotify.Artists.id == spotify.TracksArtists.artist_id)) \
                                  .join(spotify.ArtistsTags, (spotify.ArtistsTags.artist_id == spotify.Artists.id)) \
                                  .filter(spotify.ArtistsTags.tag_id == spotify.Tags.getId(tag_name)) \
                                  .all()

        return {'tracklist': res}

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
        return [i.lastfm_name for i in spotify.Artists.query.all()]
