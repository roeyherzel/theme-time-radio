from archive.models.artists import *
from archive.models.tracks import *
from archive.schemas import ArtistsSchema

from flask.views import MethodView
from flask import jsonify, render_template, request


def request_wants_json():
    best = request.accept_mimetypes.best_match(['application/json', 'text/html'])
    return best == 'application/json' and request.accept_mimetypes[best] > request.accept_mimetypes['text/html']


class ArtistAPI(MethodView):

    def get(self, artist_id):
        if artist_id is not None:
            artist = Artists.query.get(artist_id)
            res = ArtistsSchema().dump(artist)
        else:
            # return all matched artists
            artists = Artists.query.join(TracksArtists, (TracksArtists.artist_id == Artists.id)) \
                             .filter(TracksArtists.status == Status.getIdByName('matched')) \
                             .order_by(Artists.name).all()

            res = ArtistsSchema().dump(artists, many=True)

        return jsonify(res.data['data'])
