from archive.models import *
from archive.common.schemas import SongSchema, EpisodeSchema
from flask_restful import Resource, marshal_with


class SongApi(Resource):

    @marshal_with(SongSchema)
    def get(self, song_id):
        return Songs.query.get(song_id)


class SongsEpisodesApi(Resource):

    @marshal_with(EpisodeSchema)
    def get(self, song_id):
        return Episodes.query.join(Tracks, (Tracks.episode_id == Episodes.id)) \
                             .join(TracksSongs, TracksSongs.track_id == Tracks.id) \
                             .filter(TracksSongs.song_id == song_id) \
                             .filter(TracksSongs.status == Status.getIdByName('matched')) \
                             .all()
