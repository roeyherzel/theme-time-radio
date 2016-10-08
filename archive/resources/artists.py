from archive.models import *
from archive.common.schemas import ArtistSchema, AlbumSchema, SongSchema, EpisodeSchema

from flask_restful import Resource, marshal_with


class ApiArtist(Resource):

    @marshal_with(ArtistSchema)
    def get(self, artist_id=None):
        if artist_id is not None:
            return Artists.query.get(artist_id)
        else:
            return Artists.query.join(TracksArtists, (TracksArtists.artist_id == Artists.id)) \
                                .filter(TracksArtists.status == Status.getIdByName('matched')) \
                                .order_by(Artists.name) \
                                .all()


class ApiArtistsAlbums(Resource):

    @marshal_with(AlbumSchema)
    def get(self, artist_id):
        return Albums.query.join(TracksAlbums, (TracksAlbums.album_id == Albums.id)) \
                             .join(TracksArtists, (TracksArtists.track_id == TracksAlbums.track_id)) \
                             .filter(TracksArtists.artist_id == artist_id) \
                             .filter(TracksAlbums.status == Status.getIdByName('matched')) \
                             .all()


class ApiArtistsSongs(Resource):

    @marshal_with(SongSchema)
    def get(self, artist_id):
        return Songs.query.join(TracksSongs, (TracksSongs.song_id == Songs.id)) \
                          .join(TracksArtists, (TracksArtists.track_id == TracksSongs.track_id)) \
                          .filter(TracksArtists.artist_id == artist_id) \
                          .filter(TracksSongs.status == Status.getIdByName('matched')) \
                          .order_by(Songs.album_id) \
                          .all()


class ApiArtistsEpisodes(Resource):

    @marshal_with(EpisodeSchema)
    def get(self, artist_id):
        return Episodes.query.join(Tracks, (Tracks.episode_id == Episodes.id)) \
                             .join(TracksArtists, TracksArtists.track_id == Tracks.id) \
                             .filter(TracksArtists.artist_id == artist_id) \
                             .filter(TracksArtists.status == Status.getIdByName('matched')) \
                             .all()
