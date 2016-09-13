from archive.models import *
from archive.schemas import *

from flask_restful import Resource
from flask import jsonify


class Artist(Resource):

    def get(self, artist_id=None):
        if artist_id is not None:
            artist = Artists.query.get(artist_id)
            res = ArtistsSchema().dump(artist)
        else:
            # return all matched artists
            artists = Artists.query.join(TracksArtists, (TracksArtists.artist_id == Artists.id)) \
                             .filter(TracksArtists.status == Status.getIdByName('matched')) \
                             .order_by(Artists.name) \
                             .all()
            res = ArtistsSchema().dump(artists, many=True)

        return jsonify(res.data['data'])


class ArtistsReleases(Resource):

    def get(self, artist_id):
        # TODO: add distinct - list seems to be uniqe but it won't hurt to add 'distinct'
        releases = Releases.query.join(TracksReleases, (TracksReleases.release_id == Releases.id)) \
                                 .join(TracksArtists, (TracksArtists.track_id == TracksReleases.track_id)) \
                                 .filter(TracksArtists.artist_id == artist_id) \
                                 .filter(TracksReleases.status == Status.getIdByName('matched')) \
                                 .all()
        res = ReleasesSchema().dump(releases, many=True)
        return jsonify(res.data['data'])


class ArtistsEpisodes(Resource):

    def get(self, artist_id):
        episodes = Episodes.query.join(Tracks, (Tracks.episode_id == Episodes.id)) \
                                 .join(TracksArtists, TracksArtists.track_id == Tracks.id) \
                                 .filter(TracksArtists.artist_id == artist_id) \
                                 .filter(TracksArtists.status == Status.getIdByName('matched')) \
                                 .all()
        res = EpisodesSchema().dump(episodes, many=True)
        return jsonify(res.data['data'])
