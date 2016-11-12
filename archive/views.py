from flask import jsonify, render_template, request, send_file

from archive import app
from archive.models import db
from archive.models.podcast import Episodes
from archive.models.spotify import Artists

from sqlalchemy import func


# ----------- filters ----------------

import re
from jinja2 import evalcontextfilter, Markup, escape

_paragraph_re = re.compile(r'(?:\r){2,}')


@app.template_filter()
@evalcontextfilter
def nl2br(eval_ctx, value):
    result = u'\n\n'.join(u'%s' % p.replace('\n', '<br>\n') for p in _paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result


# ----------- views ----------------

@app.route('/mixtapes')
@app.route('/mixtapes/<string:tape_name>')
def mixtapes_view(tape_name=None):
    return render_template('mixtapes.html.jinja', tape_name=tape_name)


@app.route('/artists')
@app.route('/artists/<string:artist_id>')
@app.route('/artists/index/<string:index>')
def artist_view(index="A", artist_id=None):
    if artist_id:
        res = Artists.query.get(artist_id)
        # lookup artist by lastfm_name
        if res is None:
            res = Artists.query.filter(Artists.lastfm_name == artist_id).one()

        return render_template('artist.html.jinja', artist=res)

    # build uniqe list of sorted artist names index
    artists_index = [re.sub(r"[^a-zA-Z]", "0", i.name[0].upper()) for i in Artists.query.order_by(Artists.name).all()]
    artists_index = sorted(set(artists_index))

    # get artist objects matching index
    index = index.upper()
    if index == "0":
        # didn't find a method to performe the filtering in db query
        artists = [a for a in Artists.query.all() if re.match(r"[^a-zA-Z]", a.name[0])]
    else:
        artists = Artists.query.order_by(Artists.name).filter(func.upper(Artists.name).startswith(index)).all()

    return render_template('all_artists.html.jinja', artists=artists, index=index, index_list=artists_index)


@app.route('/episodes')
@app.route('/episodes/season/<int:season>')
@app.route('/episodes/<int:episode_id>')
def episode_view(episode_id=None, season=1):
    if episode_id:
        res = Episodes.query.get(episode_id)
        return render_template('episode.html.jinja', episode=res, prev=res.prev, next=res.next)

    episodes = Episodes.query.filter(Episodes.season == season).order_by(Episodes.id)
    return render_template('all_episodes.html.jinja', episodes=episodes, season=season, seasons=[1, 2, 3])


@app.route('/about')
def about():
    return render_template('about.html.jinja')


@app.route('/')
def index():
    return render_template('index.html.jinja')
