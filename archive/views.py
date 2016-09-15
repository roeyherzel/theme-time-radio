from flask import jsonify, render_template, request

from archive import app
from archive.models import *
from archive.schemas import *

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


@app.route('/artists/<int:artist_id>')
def artist_detail(artist_id):
    artist = Artists.query.get(artist_id)
    res = ArtistsSchema().dump(artist)
    return render_template('artist_detail.html', artist=res.data['data'])


@app.route('/episodes/<int:episode_id>')
def episode_detail(episode_id):
    ep = Episodes.query.get(episode_id)
    # res = EpisodesSchema().dump(ep).data
    print(ep)
    return render_template('episode_detail.html', ep=ep)  # res['data'])


@app.route('/')
def index():
    ep_latest = Episodes.query.order_by(Episodes.date_pub).limit(6).all()

    # FIXME: this query returns 23 insted of 21
    # this is because date_pub has to be in the select statment because of order_by
    subq = db.session.query(distinct(TracksArtists.artist_id).label("artist_id"), Episodes.date_pub) \
                     .filter(TracksArtists.status == 1) \
                     .join(Tracks) \
                     .join(Episodes) \
                     .order_by(desc(Episodes.date_pub)) \
                     .subquery()

    db.session.query(Artists).join(subq, Artists.id == subq.c.artist_id).all()

    return render_template('index.html')
