from archive.models import *
from archive.common.schemas import ReleaseSchema, ArtistSchema, EpisodeSchema
from archive.common.utils import limit_query

from flask_restful import Resource, marshal_with, reqparse


class ApiRelease(Resource):

    @marshal_with(ReleaseSchema)
    def get(self, release_id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('limit', type=int, help="limit query results")
        args = parser.parse_args()

        if release_id is not None:
            return Releases.query.get(release_id)
        else:
            myQuery = Releases.query.join(TracksReleases, (TracksReleases.release_id == Releases.id)) \
                                    .filter(TracksReleases.status == Status.getIdByName('matched')) \
                                    .order_by(Releases.title)

            return limit_query(myQuery, args.get('limit')).all()


class ApiReleasesArtists(Resource):

    @marshal_with(ArtistSchema)
    def get(self, release_id):
        return Artists.query.join(TracksArtists, (TracksArtists.artist_id == Artists.id)) \
                            .join(TracksReleases, (TracksReleases.track_id == TracksArtists.track_id)) \
                            .filter(TracksReleases.release_id == release_id) \
                            .filter(TracksArtists.status == Status.getIdByName('matched')) \
                            .all()


class ApiReleasesEpisodes(Resource):

    @marshal_with(EpisodeSchema)
    def get(self, release_id):
        return Episodes.query.join(Tracks, (Tracks.episode_id == Episodes.id)) \
                             .join(TracksReleases, TracksReleases.track_id == Tracks.id) \
                             .filter(TracksReleases.release_id == release_id) \
                             .filter(TracksReleases.status == Status.getIdByName('matched')) \
                             .all()
