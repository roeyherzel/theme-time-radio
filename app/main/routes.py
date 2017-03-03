from flask import render_template, abort
from . import main
from ..models import Episodes, Tracks, Artists, Tags
from sqlalchemy import func
import re


"""
-----------------------------------------------------------------------------------------------------
Error handlers
-----------------------------------------------------------------------------------------------------
"""


@main.errorhandler(404)
def not_found_error(error):
    return render_template('404.html.j2'), 404


"""
-----------------------------------------------------------------------------------------------------
Views
-----------------------------------------------------------------------------------------------------
"""


@main.route('/tags')
@main.route('/tags/<string:tag>')
def tags_view(tag=None):
    return render_template('tag_info.html.j2', tag=tag)


@main.route('/artists/<string:id>')
@main.route('/artists/name/<string:name>')
def artist_view(id=None, name=None):
    if id:
        artist = Artists.query.get(id)

    elif name:
        artist = Artists.query.filter(func.lower(Artists.lastfm_name) == name.lower()) \
                        .one_or_none()

    if artist is None:
        abort(404)
    else:
        return render_template('artist_info.html.j2', artist=artist)


@main.route('/artists')
@main.route('/artists/index/<string:index>')
def all_artists_view(index="A"):
    # build uniqe list of sorted artist names index
    artists_index = [re.sub(r"[^a-zA-Z]", "0", i.name[0].upper()) for i in Artists.query.order_by(Artists.name).all()]
    artists_index = sorted(set(artists_index))

    if index not in artists_index:
        abort(404)

    # get artist objects matching index
    index = index.upper()
    if index == "0":
        # didn't find a method to performe the filtering in db query, filter all NON(^) A-Z
        artists = [a for a in Artists.query.all() if re.match(r"[^a-zA-Z]", a.name[0])]
    else:
        artists = Artists.query.order_by(Artists.name).filter(func.upper(Artists.name).startswith(index)).all()

    return render_template('all_artists.html.j2', artists=artists, index=index, index_list=artists_index)


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
        'tags': "{:,}".format(Tags.query.count())
    }
    return render_template('index.html.j2', stats=stats)
