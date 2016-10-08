from archive.models import *
from archive.common.schemas import AlbumSchema, ArtistSchema, EpisodeSchema
from archive.common.utils import limit_query

from flask_restful import Resource, marshal_with, reqparse


class ApiAlbum(Resource):

    @marshal_with(AlbumSchema)
    def get(self, album_id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('limit', type=int, help="limit query results")
        args = parser.parse_args()

        if album_id is not None:
            return Albums.query.get(album_id)
        else:
            myQuery = Albums.query.join(TracksAlbums, (TracksAlbums.album_id == Albums.id)) \
                                    .filter(TracksAlbums.status == Status.getIdByName('matched')) \
                                    .order_by(Albums.title)

            return limit_query(myQuery, args.get('limit')).all()


class ApiAlbumsArtists(Resource):

    @marshal_with(ArtistSchema)
    def get(self, album_id):
        return Artists.query.join(TracksArtists, (TracksArtists.artist_id == Artists.id)) \
                            .join(TracksAlbums, (TracksAlbums.track_id == TracksArtists.track_id)) \
                            .filter(TracksAlbums.album_id == album_id) \
                            .filter(TracksArtists.status == Status.getIdByName('matched')) \
                            .all()


class ApiAlbumsEpisodes(Resource):

    @marshal_with(EpisodeSchema)
    def get(self, album_id):
        return Episodes.query.join(Tracks, (Tracks.episode_id == Episodes.id)) \
                             .join(TracksAlbums, TracksAlbums.track_id == Tracks.id) \
                             .filter(TracksAlbums.album_id == album_id) \
                             .filter(TracksAlbums.status == Status.getIdByName('matched')) \
                             .all()
