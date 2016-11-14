
from archive.models import db
from archive.models.spotify import *
from archive.models.podcast import *
from archive.resources import schemas

from flask_restful import Resource, reqparse, marshal_with
from sqlalchemy import desc, distinct, func

from archive import api


parser = reqparse.RequestParser()
parser.add_argument('limit', type=str, help="limit query results")
parser.add_argument('random', type=str, help="limit query results")


@api.resource('/api/tags', '/api/tags/<string:tag_name>')
class TagsAPI(Resource):

    @marshal_with(schemas.TagsCount().as_dict)
    def get(self, tag_name=None):
        args = parser.parse_args()

        res = Tags.getAllValid()
        if tag_name:
            res = res.filter(Tags.name == tag_name).first()
            return {'tag': res[0], 'track_count': res[1]}

        if args.get('random'):
            res = res.order_by(func.random())
        else:
            res = res.order_by(desc('track_count'))

        if args.get('limit'):
            res = res.limit(args.get('limit'))

        return [{'tag': i.Tags, 'track_count': i.track_count} for i in res.all()]


@api.resource('/api/tags/<string:tag_name>/artists')
class TagsArtistsAPI(Resource):

    @marshal_with(schemas.Artist().as_dict)
    def get(self, tag_name):
        return Artists.query.join(ArtistsTags, ArtistsTags.artist_id == Artists.id) \
                            .join(Tags, (Tags.id == ArtistsTags.tag_id)) \
                            .join(TracksArtists, (TracksArtists.artist_id == ArtistsTags.artist_id)) \
                            .join(Tracks, (Tracks.id == TracksArtists.track_id)) \
                            .filter(Tracks.spotify_song) \
                            .filter(Tags.name == tag_name) \
                            .all()


@api.resource('/api/tags/<string:tag_name>/tracklist')
class TagsTracksAPI(Resource):

    @marshal_with(schemas.ArtistTracklist().as_dict)
    def get(self, tag_name):
        args = parser.parse_args()

        res = Tracks.query.join(TracksArtists, (TracksArtists.track_id == Tracks.id)) \
                          .join(Artists, (Artists.id == TracksArtists.artist_id)) \
                          .join(ArtistsTags, (ArtistsTags.artist_id == Artists.id)) \
                          .filter(ArtistsTags.tag_id == Tags.getId(tag_name))

        return {'tracklist': res.all()}
