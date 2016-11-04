from flask import jsonify, render_template, request, send_file

from archive import app
from archive.models import db
from archive.models.podcast import Episodes
from archive.models.spotify import Artists

from sqlalchemy import func

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
    if artist_id is not None:
        res = Artists.query.get(artist_id)
        if res is None:
            res = Artists.query.filter(Artists.lastfm_name == artist_id).one()
        return render_template('artist.html.jinja', artist=res)

    index = index.upper()
    artists_names = db.session.query(Artists.name).order_by(Artists.name).all()

    # build uniqe list of sorted artist names index
    artists_index = [re.sub(r"[^a-zA-Z]", "0", i[0][0].upper()) for i in artists_names]
    artists_index = sorted(set(artists_index))

    # get artist objects matching index
    if index == "0":
        # didn't find a method to performe the filtering in db query
        artists = [a for a in Artists.query.all() if re.match(r"[^a-zA-Z]", a.name[0])]
    else:
        artists = Artists.query.order_by(Artists.name).filter(func.upper(Artists.name).startswith(index)).all()

    print(artists)
    return render_template('all_artists.html.jinja', artists=artists, index_list=artists_index)


@app.route('/episodes')
@app.route('/episodes/<int:episode_id>')
def episode_view(episode_id=None):
    if episode_id is None:
        return render_template('all_episodes.html.jinja')

    res = Episodes.query.get(episode_id)
    return render_template('episode.html.jinja', episode=res)


@app.route('/')
def index():
    return render_template('index.html.jinja')
