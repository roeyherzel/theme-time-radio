from flask import render_template, abort
from . import main
from ..models import Episodes, Tracks, Artists, Tags
from sqlalchemy import func
import re


@main.errorhandler(404)
def not_found_error(error):
    return render_template('404.html.j2'), 404


@main.route('/genres')
@main.route('/genres/<string:genre>')
def genres_view(genre=None):
    if genre is None:
        return render_template('genres.html.j2')
    else:
        return render_template('genre_info.html.j2', genre=genre)


@main.route('/artists')
@main.route('/artists/<string:id>')
@main.route('/artists/name/<string:name>')
def artist_view(id=None, name=None):
    if id is None and name is None:
        return render_template('artists.html.j2')
    elif id:
        artist = Artists.query.get(id)
    elif name:
        artist = Artists.query.filter(func.lower(Artists.lastfm_name) == name.lower()) \
                        .one_or_none()

    return render_template('artist_info.html.j2', artist=artist)


@main.route('/episodes')
@main.route('/episodes/season/<int:season>')
@main.route('/episodes/<int:id>')
def episode_view(id=None, season=1):
    if id:
        episode = Episodes.query.get(id)
        if episode is None:
            abort(404)

        return render_template('episode_info.html.j2', episode=episode, prev=episode.prev, next=episode.next)

    seasons = [1, 2, 3]
    if season not in seasons:
        abort(404)

    episodes = Episodes.query.filter(Episodes.season == season).order_by(Episodes.id)
    return render_template('all_episodes.html.j2', episodes=episodes, season=season, seasons=seasons)


@main.route('/about')
def about():
    return render_template('about.html.j2')


@main.route('/')
def index():
    stats = {
        'episodes': "{:,}".format(Episodes.query.count()),
        'songs': "{:,}".format(Tracks.query.count()),
        'artists': "{:,}".format(Artists.query.count()),
        'genres': "{:,}".format(genres.query.count())
    }
    return render_template('index.html.j2', stats=stats)
