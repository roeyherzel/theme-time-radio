
from archive.models import spotify, podcast, db
from archive.common.utils import limit_query
from archive.resources import schemas

from flask_restful import Resource, reqparse, marshal, marshal_with, marshal_with_field, fields
from sqlalchemy import desc, distinct, func

from archive import api


parser = reqparse.RequestParser()
parser.add_argument('limit', type=str, help="limit query results")
parser.add_argument('all', default=False, type=bool, help="disables filtering")


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


@api.resource('/api/tags', '/api/tags/<string:tag_name>')
class TagsAPI(Resource):

    @marshal_with(schemas.Tags().as_dict)
    def get(self, tag_name=None):
        args = parser.parse_args()

        if args.get('all') is True:
            return spotify.Tags.query.all()

        res = db.session.query(spotify.Tags, func.count(podcast.Tracks.id).label('track_count')) \
                        .join(spotify.ArtistsTags, (spotify.ArtistsTags.tag_id == spotify.Tags.id)) \
                        .join(spotify.TracksArtists, (spotify.TracksArtists.artist_id == spotify.ArtistsTags.artist_id)) \
                        .join(podcast.Tracks, (podcast.Tracks.id == spotify.TracksArtists.track_id)) \
                        .filter(podcast.Tracks.spotify_song) \
                        .group_by(spotify.Tags)

        if tag_name is not None:
            res = res.filter(spotify.Tags.name == tag_name).first()
            return {'tag': res[0], 'track_count': res[1]}
        else:
            res = res.all()
            return [{'tag': i[0], 'track_count': i[1]} for i in res]


@api.resource('/api/tags/<string:tag_name>/artists')
class TagsArtistsAPI(Resource):

    @marshal_with(schemas.Artist().as_dict)
    def get(self, tag_name):

        return spotify.Artists.query.join(spotify.ArtistsTags, spotify.ArtistsTags.artist_id == spotify.Artists.id) \
                                    .join(spotify.Tags, (spotify.Tags.id == spotify.ArtistsTags.tag_id)) \
                                    .filter(spotify.Tags.name == tag_name) \
                                    .all()


@api.resource('/api/tags/<string:tag_name>/tracklist')
class TagsTracksAPI(Resource):

    @marshal_with(schemas.ArtistTracklist().as_dict)
    def get(self, tag_name):
        args = parser.parse_args()

        res = podcast.Tracks.query.join(spotify.TracksArtists, (spotify.TracksArtists.track_id == podcast.Tracks.id)) \
                                  .join(spotify.Artists, (spotify.Artists.id == spotify.TracksArtists.artist_id)) \
                                  .join(spotify.ArtistsTags, (spotify.ArtistsTags.artist_id == spotify.Artists.id)) \
                                  .filter(spotify.ArtistsTags.tag_id == spotify.Tags.getId(tag_name))

        if args.get('all') is not True:
            res = res.filter(podcast.Tracks.spotify_song)

        return {'tracklist': res.all()}

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
