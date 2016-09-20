from archive.models import *
from archive.common.schemas import ReleaseSchema, ArtistSchema

from flask_restful import Resource, marshal_with


class Release(Resource):

    @marshal_with(ReleaseSchema)
    def get(self, release_id=None):
        if release_id is not None:
            return Releases.query.get(release_id)
        else:
            return Releases.query.join(TracksReleases, (TracksReleases.release_id == Releases.id)) \
                                 .filter(TracksReleases.status == Status.getIdByName('matched')) \
                                 .order_by(Releases.title).all()


class ReleasesArtists(Resource):

    @marshal_with(ArtistSchema)
    def get(self, release_id):
        return Artists.query.join(TracksArtists, (TracksArtists.artist_id == Artists.id)) \
                            .join(TracksReleases, (TracksReleases.track_id == TracksArtists.track_id)) \
                            .filter(TracksReleases.release_id == release_id) \
                            .filter(TracksArtists.status == Status.getIdByName('matched')) \
                            .all()
