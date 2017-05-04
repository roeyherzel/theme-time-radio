from flask_restful import Resource, reqparse, marshal_with, marshal_with_field, fields, abort
from . import api
from . import schemas
from ..models import *
from sqlalchemy import func


@api.resource('/api/artists')
class API_AllArtists(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('limit', type=str, help="limit query results")
    parser.add_argument('random', type=bool, help="random query results")

    @marshal_with(schemas.Artist().as_dict)
    def get(self):
        args = __class__.parser.parse_args()
        query = Artists.query

        if args.get('random'):
            query = query.order_by(func.random())
        else:
            query = query.order_by(Artists.name)

        if args.get('limit'):
            # filter only artists with images
            query = query.filter(Artists.lastfm_image != None, Artists.lastfm_image != '') \
                         .limit(args.get('limit'))

        return query.all() or abort(500)


@api.resource('/api/artists/<string:artist>')
class API_Artist(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('lastfm', type=bool, help="Lookup artist by lastfm name")

    @marshal_with(schemas.Artist().as_dict)
    def get(self, artist):
        args = args = __class__.parser.parse_args()
        query = Artists.query

        if args.get('lastfm'):
            query = query.filter(Artists.lastfm_name == artist).one_or_none()
        else:
            query = query.get(artist)

        return query or abort(404)


@api.resource('/api/artists/<string:artist_id>/episodes')
class API_ArtistsEpisodes(Resource):

    @marshal_with(schemas.Episode().as_dict)
    def get(self, artist_id):
        return Episodes.query.join(Tracks, Tracks.episode_id == Episodes.id) \
                             .join(aux_tracks_artists, aux_tracks_artists.c.track_id == Tracks.id) \
                             .filter(aux_tracks_artists.c.artist_id == artist_id) \
                             .order_by(Tracks.episode_id, Tracks.position) \
                             .all()


@api.resource('/api/artists/<string:artist_id>/tracklist')
class API_ArtistsTracklist(Resource):

    @marshal_with(schemas.Track().as_dict)
    def get(self, artist_id):
        return Artists.query.get(artist_id).tracks


@api.resource('/api/helper/all-lastfm-artists')
class LastFmArtistsAPI(Resource):

    @marshal_with_field(fields.List(fields.String()))
    def get(self):
        return [i.lastfm_name for i in Artists.query.all()]


@api.resource('/api/genres', '/api/genres/<string:tag_name>')
class TagsAPI(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('limit', type=str, help="limit query results")
    parser.add_argument('random', type=str, help="limit query results")

    @marshal_with(schemas.Tags().as_dict)
    def get(self, tag_name=None):
        if tag_name is None:
            args = __class__.parser.parse_args()
            query = Tags.query
            query = query.order_by(func.random()) if args.get('random') else query.order_by(Tags.name)
            query = query.limit(args.get('limit')) if args.get('limit') else query

            return query.all()
        else:
            return Tags.query.filter(Tags.name == tag_name).first()


@api.resource('/api/genres/<string:tag>/artists')
class TagsArtistsAPI(Resource):

    @marshal_with(schemas.Artist().as_dict)
    def get(self, tag):
        return Artists.query.join(aux_artists_tags, aux_artists_tags.c.artist_id == Artists.id) \
                            .filter(aux_artists_tags.c.tag_id == Tags.getId(tag)) \
                            .all()


@api.resource('/api/genres/<string:tag>/tracklist')
class TagsTracklistAPI(Resource):

    @marshal_with(schemas.Track().as_dict)
    def get(self, tag):
        return Tracks.query.join(aux_tracks_artists, aux_tracks_artists.c.track_id == Tracks.id) \
                           .join(aux_artists_tags, aux_artists_tags.c.artist_id == aux_tracks_artists.c.artist_id) \
                           .filter(aux_artists_tags.c.tag_id == Tags.getId(tag)) \
                           .order_by(Tracks.episode_id, Tracks.position) \
                           .all()
