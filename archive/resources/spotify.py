
from archive.models import spotify, podcast, db
from archive.resources import schemas

from flask_restful import Resource, reqparse, marshal, marshal_with, marshal_with_field, fields
from sqlalchemy import desc, distinct, func

from archive import api


parser = reqparse.RequestParser()
parser.add_argument('limit', type=str, help="limit query results")
parser.add_argument('random', type=str, help="limit query results")
parser.add_argument('all', default=False, type=bool, help="disables filtering")


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
        return [t for t in res if t.artists.count() > 4 and t.artists.count() < 70]


@api.resource('/api/tags', '/api/tags/<string:tag_name>')
class TagsAPI(Resource):

    @marshal_with(schemas.TagsCount().as_dict)
    def get(self, tag_name=None):
        args = parser.parse_args()

        if args.get('all') is True:
            return spotify.Tags.query.all()

        # NOTE: WORKAROUND: issue with spotifyPlayer with more then 70 songs
        res = db.session.query(spotify.Tags, func.count(podcast.Tracks.id).label('track_count')) \
                        .join(spotify.ArtistsTags, (spotify.ArtistsTags.tag_id == spotify.Tags.id)) \
                        .join(spotify.TracksArtists, (spotify.TracksArtists.artist_id == spotify.ArtistsTags.artist_id)) \
                        .join(podcast.Tracks, (podcast.Tracks.id == spotify.TracksArtists.track_id)) \
                        .filter(podcast.Tracks.spotify_song) \
                        .group_by(spotify.Tags) \
                        .having(func.count(podcast.Tracks.id) < 70) \
                        .having(func.count(podcast.Tracks.id) > 4)

        if tag_name:
            res = res.filter(spotify.Tags.name == tag_name).first()
            return {'tag': res[0], 'track_count': res[1]}

        if args.get('random'):
            res = res.order_by(func.random())
        else:
            res = res.order_by(desc('track_count'))

        if args.get('limit'):
            res = res.limit(args.get('limit'))

        return [{'tag': i.Tags, 'track_count': i.track_count} for i in res.all()]


@api.resource('/api/tags/<string:tag_name>/artists')
class TagsArtistsAPI(Resource):

    @marshal_with(schemas.Artist().as_dict)
    def get(self, tag_name):

        return spotify.Artists.query.join(spotify.ArtistsTags, spotify.ArtistsTags.artist_id == spotify.Artists.id) \
                                    .join(spotify.Tags, (spotify.Tags.id == spotify.ArtistsTags.tag_id)) \
                                    .join(spotify.TracksArtists, (spotify.TracksArtists.artist_id == spotify.ArtistsTags.artist_id)) \
                                    .join(podcast.Tracks, (podcast.Tracks.id == spotify.TracksArtists.track_id)) \
                                    .filter(podcast.Tracks.spotify_song) \
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
