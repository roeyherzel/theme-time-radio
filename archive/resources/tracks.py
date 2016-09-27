from archive.common.utils import limit_api_results
from archive.common.schemas import TrackSchema
from archive.models import *

from flask_restful import Resource, abort, reqparse, marshal_with

from sqlalchemy import desc
from sqlalchemy.orm.exc import NoResultFound


class TrackApi(Resource):

    @marshal_with(TrackSchema)
    def get(self, track_id):
        return Tracks.query.get(track_id)


parser = reqparse.RequestParser()
parser.add_argument('id')


class TracksArtistsApi(Resource):

    def post(self, track_id):
        args = parser.parse_args()
        artist_id = args.id

        try:
            myTrack = TracksArtists.query.filter_by(track_id=track_id, artist_id=artist_id).one()

        except NoResultFound as err:
            abort(404, message="didn't find pending resource with track_id({}) and artist_id({})".format(track_id,
                                                                                                         artist_id))

        myTrack.status = Status.getIdByName('matched')
        TracksArtists.update(myTrack)
        print("match - updated track_id({}) -> artist_id({}): status(matched)".format(artist_id, track_id))

        TracksArtists.query.filter_by(track_id=track_id) \
                           .filter(TracksArtists.status != Status.getIdByName('matched')) \
                           .delete()

        print("match - deleting all other pending")
        db.session.commit()
        print("match - commited")

        return artist_id, 201


class TracksReleasesApi(Resource):

    def post(self, track_id):
        args = parser.parse_args()
        release_id = args.id

        try:
            myTrack = TracksReleases.query.filter_by(track_id=track_id, release_id=release_id).one()

        except NoResultFound as err:
            print("match - 404, didn't find pending")
            abort(404, message="didn't find pending resource with track_id({}) and release_id({})".format(track_id,
                                                                                                          release_id))

        myTrack.status = Status.getIdByName('matched')
        TracksReleases.update(myTrack)
        print("match - updated track_id({}) -> release_id({}): status(matched)".format(release_id, track_id))

        TracksReleases.query.filter_by(track_id=track_id) \
                            .filter(TracksReleases.status != Status.getIdByName('matched')) \
                            .delete()

        print("match - deleting all other pending")
        db.session.commit()
        print("match - commited")

        return release_id, 201
