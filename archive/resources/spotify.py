
from archive.models import spotify, podcast, db
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
            return spotify.Artists.query.get(artist_id)

        order = func.random() if args.get('random') else spotify.Artists.name

        res = spotify.Artists.query.order_by(order)
        if args.get('limit'):
            res = res.limit(args.get('limit'))

        return res.all()


@api.resource('/api/artists/<string:artist_id>/episodes')
class ArtistsEpisodesAPI(Resource):

    @marshal_with(schemas.Episode().as_dict)
    def get(self, artist_id):
        return podcast.Episodes.query.join(podcast.Tracks, podcast.Tracks.episode_id == podcast.Episodes.id) \
                               .join(spotify.TracksArtists, spotify.TracksArtists.track_id == podcast.Tracks.id) \
                               .filter(spotify.TracksArtists.artist_id == artist_id) \
                               .all()


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

    @marshal_with(schemas.Tags().as_dict)
    def get(self, artist_id):
        res = spotify.Tags.query.join(spotify.ArtistsTags, (spotify.ArtistsTags.tag_id == spotify.Tags.id)) \
                                .join(spotify.TracksArtists, (spotify.TracksArtists.artist_id == spotify.ArtistsTags.artist_id)) \
                                .join(podcast.Tracks, (podcast.Tracks.id == spotify.TracksArtists.track_id)) \
                                .filter(spotify.ArtistsTags.artist_id == artist_id) \
                                .filter(podcast.Tracks.spotify_song) \
                                .all()

        # NOTE: WORKAROUND: issue with spotifyPlayer with more then 70 songs
        return [t for t in res if t.artists.count() >= 5 and t.artists.count() <= 70]


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
