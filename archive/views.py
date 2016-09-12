from flask import jsonify, render_template, request
from flask.views import MethodView

from archive import app
from archive.models import *
from archive.schemas import *

from archive.resources.artists import ArtistAPI
from archive.resources.releases import ReleaseAPI

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


artist_view = ArtistAPI.as_view('artist_api')
app.add_url_rule('/api/artists', defaults={'artist_id': None}, view_func=artist_view)
app.add_url_rule('/api/artists/<int:artist_id>', view_func=artist_view)


release_view = ReleaseAPI.as_view('release_api')
app.add_url_rule('/api/releases', defaults={'release_id': None}, view_func=release_view)
app.add_url_rule('/api/releases/<int:release_id>', view_func=release_view)


@app.route('/songs/<string:song_id>')
def song_detail(song_id):
    song = Songs.query.get(song_id)
    res = SongsSchema().dump(song)
    return jsonify(res.data)


@app.route('/episodes')
def episodes_list():
    ep = Episodes.query.order_by(Episodes.date_pub).all()
    res = EpisodesSchema().dump(ep, many=True)
    return jsonify(res.data['data'])


@app.route('/episode/<int:episode_id>/tracklist')
def episode_tracklist(episode_id):
    ep = Episodes.query.get(episode_id)
    res = EpisodesTracklistScheam().dump(ep)
    return jsonify(res.data['data']['attributes']['tracklist']['data'])

# ----------------------------------------------------------
# Views
# ----------------------------------------------------------


@app.route('/artists/<int:artist_id>')
def artist_detail(artist_id):
    artist = Artists.query.get(artist_id)
    res = ArtistsSchema().dump(artist).data
    return render_template('artist_detail.html', artist=res['data'])


@app.route('/episodes/<int:episode_id>')
def episode_detail(episode_id):
    ep = Episodes.query.get(episode_id)
    res = EpisodesSchema().dump(ep).data
    return render_template('episode_detail.html', ep=res['data'])


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
