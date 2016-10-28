from flask import jsonify, render_template, request, send_file

from archive import app
from archive.models.podcast import Episodes
from archive.models.spotify import SpotifyArtists

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

@app.route('/artists/<string:artist_id>')
def artist_view(artist_id):
    res = SpotifyArtists.query.get(artist_id)
    if res is None:
        res = SpotifyArtists.query.filter(SpotifyArtists.lastfm_name == artist_id).one()
    return render_template('artist.html.jinja', artist=res)


@app.route('/artists')
def all_artists_view():
    return render_template('all_artists.html.jinja')


@app.route('/episodes/<int:episode_id>')
def episode_view(episode_id):
    res = Episodes.query.get(episode_id)
    return render_template('episode.html.jinja', episode=res)


@app.route('/')
def index():
    return render_template('index.html.jinja')
