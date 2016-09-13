from archive.models import *
from archive.schemas import ReleasesSchema

from flask_restful import Resource
from flask import jsonify


class Release(Resource):

    def get(self, release_id=None):
        if release_id is not None:
            release = Releases.query.get(release_id)
            res = ReleasesSchema().dump(release)
        else:
            releases = Releases.query.join(TracksReleases, (TracksReleases.release_id == Releases.id)) \
                               .filter(TracksReleases.status == Status.getIdByName('matched')) \
                               .order_by(Releases.title).all()

            res = ReleasesSchema().dump(releases, many=True)

        return jsonify(res.data['data'])
