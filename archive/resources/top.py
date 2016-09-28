from archive.models import *
from archive.common.schemas import TopReleaseSchema
from archive.common.utils import limit_query

from flask_restful import Resource, marshal_with, reqparse
from sqlalchemy import desc, func


class ApiTopRelease(Resource):

    @marshal_with(TopReleaseSchema)
    def get(self, release_id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('limit', type=int, help="limit query results")
        args = parser.parse_args()

        myQuery = db.session.query(TracksReleases.release_id.label('release_id'),
                                   func.count(TracksReleases.track_id).label('play_count')) \
                            .group_by(TracksReleases.release_id) \
                            .order_by(func.count(TracksReleases.track_id).desc())

        myQuery = limit_query(myQuery, args.get('limit')).all()
        myQuery = [dict({'release_id': i.release_id, 'play_count': i.play_count}) for i in myQuery]
        return myQuery
