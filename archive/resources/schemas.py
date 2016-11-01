from flask import url_for
from flask_restful import fields


class Base(object):
    @property
    def as_dict(self):
        return self.__dict__


class SpotifyResource(Base):
    def __init__(self):
        self.id = fields.String
        self.name = fields.String


class Tags(Base):
    def __init__(self):
        self.id = fields.Integer
        self.name = fields.String
        self.type = fields.String


class ArtistTags(SpotifyResource):
    def __init__(self):
        super().__init__()
        self.tags = fields.List(fields.Nested({'tag': fields.Nested(Tags().as_dict)}))


class Artist(SpotifyResource):
    def __init__(self):
        super().__init__()
        self.view = fields.FormattedString("artists/{id}")
        self.lastfm_name = fields.String
        self.lastfm_image = fields.String


class Album(SpotifyResource):
    def __init__(self):
        super().__init__()


class Song(SpotifyResource):
    def __init__(self):
        super().__init__()
        self.preview_url = fields.String
        # self.album = Album().as_dict


class Episode(Base):
    def __init__(self):
        self.id = fields.Integer
        self.view = fields.FormattedString("episodes/{id}")
        self.api = fields.FormattedString("api/episodes/{id}")
        self.title = fields.String
        self.season = fields.Integer
        self.image = fields.String


class Track(Base):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)

        self.id = fields.Integer
        self.resolved = fields.Boolean
        self.title = fields.String
        self.parsed_song = fields.String
        self.parsed_artist = fields.String
        self.position = fields.Integer
        self.year = fields.Integer
        self.spotify_artists = fields.List(fields.Nested({'artist': fields.Nested(Artist().as_dict)}))
        self.spotify_song = fields.Nested({'song': fields.Nested(Song().as_dict)})


class EpisodeTracklist(Base):
    def __init__(self):
        myTrack = Track().as_dict
        self.tracklist = fields.List(fields.Nested(myTrack))


class ArtistTracklist(Base):
    def __init__(self):
        myTrack = Track(episode=fields.Nested(Episode().as_dict)).as_dict
        self.tracklist = fields.List(fields.Nested(myTrack))
