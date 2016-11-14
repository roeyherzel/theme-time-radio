from archive.models import db
from archive.models.spotify import *
from archive.models.podcast import *
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
            res = res.limit(args.get('limit'))

        return res.all()


@api.resource('/api/artists/<string:artist_id>/episodes')
class ArtistsEpisodesAPI(Resource):

    @marshal_with(schemas.Episode().as_dict)
    def get(self, artist_id):
        return Episodes.query.join(Tracks, Tracks.episode_id == Episodes.id) \
                             .join(TracksArtists, TracksArtists.track_id == Tracks.id) \
                             .filter(TracksArtists.artist_id == artist_id) \
                             .all()


@api.resource('/api/artists/<string:artist_id>/tracklist')
class ArtistsTracklistAPI(Resource):

    @marshal_with(schemas.ArtistTracklist().as_dict)
    def get(self, artist_id):
        res = Tracks.query.join(TracksArtists, (Tracks.id == TracksArtists.track_id)) \
                          .filter(TracksArtists.artist_id == artist_id) \
                          .all()
        return {'tracklist': res}


@api.resource('/api/artists/<string:artist_id>/tags')
class ArtistsTagsAPI(Resource):

    @marshal_with(schemas.Tags().as_dict)
    def get(self, artist_id):
        # NOTE: WORKAROUND: issue with spotifyPlayer with more then 70 songs
        res = db.session.query(Tags, func.count(Tracks.id).label('track_count')) \
                        .join(ArtistsTags, (ArtistsTags.tag_id == Tags.id)) \
                        .join(TracksArtists, (TracksArtists.artist_id == ArtistsTags.artist_id)) \
                        .join(Tracks, (Tracks.id == TracksArtists.track_id)) \
                        .filter(Tracks.spotify_song) \
                        .group_by(Tags) \
                        .having(func.count(Tracks.id) <= 70) \
                        .having(func.count(Tracks.id) >= 5)

        return [i[0] for i in res.all() if i[0].artists.filter(ArtistsTags.artist_id == artist_id).count() > 0]

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
