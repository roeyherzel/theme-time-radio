
from archive.models import spotify, podcast, db
from archive.resources import schemas

from flask_restful import Resource, reqparse, marshal_with
from sqlalchemy import desc, distinct, func

from archive import api


parser = reqparse.RequestParser()
parser.add_argument('limit', type=str, help="limit query results")
parser.add_argument('random', type=str, help="limit query results")


@api.resource('/api/tags', '/api/tags/<string:tag_name>')
class TagsAPI(Resource):

    @marshal_with(schemas.TagsCount().as_dict)
    def get(self, tag_name=None):
        args = parser.parse_args()

        # NOTE: WORKAROUND: issue with spotifyPlayer with more then 70 songs
        res = db.session.query(spotify.Tags, func.count(podcast.Tracks.id).label('track_count')) \
                        .join(spotify.ArtistsTags, (spotify.ArtistsTags.tag_id == spotify.Tags.id)) \
                        .join(spotify.TracksArtists, (spotify.TracksArtists.artist_id == spotify.ArtistsTags.artist_id)) \
                        .join(podcast.Tracks, (podcast.Tracks.id == spotify.TracksArtists.track_id)) \
                        .filter(podcast.Tracks.spotify_song) \
                        .group_by(spotify.Tags) \
                        .having(func.count(podcast.Tracks.id) <= 70) \
                        .having(func.count(podcast.Tracks.id) >= 5)

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

        return {'tracklist': res.all()}
