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
        print("pending - updated track id({}) to status(matched)".format(track_id))

        TracksArtists.query.filter_by(track_id=track_id) \
                           .filter(TracksArtists.status != Status.getIdByName('matched')) \
                           .delete()

        print("pending - delete pending")
        db.session.commit()
        print("pending - commit")

        return artist_id, 201
