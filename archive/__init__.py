from flask import Flask, jsonify, render_template, request
from archive.models import *
from archive.schemas import *

import re
from jinja2 import evalcontextfilter, Markup, escape


app = Flask(__name__)
app.config.from_object('config')


_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')


@app.template_filter()
@evalcontextfilter
def nl2br(eval_ctx, value):
    result = u'\n\n'.join(u'%s' % p.replace('\n', '<br>\n') for p in _paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result


db.init_app(app)


# ----------------------------------------------------------
# API
# ----------------------------------------------------------


@app.route('/api/artists')
def artists_list():
    ep = Artists.query.join(TracksArtists, (TracksArtists.artist_id == Artists.id)) \
                      .filter(TracksArtists.status == Status.getIdByName('matched')).order_by(Artists.name).all()
    res = ArtistsSchema().dump(ep, many=True).data
    return jsonify(res)


@app.route('/api/artists/<int:artist_id>')
def artist_detail(artist_id):
    artist = Artists.query.get(artist_id)
    res = ArtistsSchema().dump(artist)
    return jsonify(res.data)


@app.route('/api/releases/<int:release_id>')
def release_detail(release_id):
    release = Releases.query.get(release_id)
    res = ReleasesSchema().dump(release)
    return jsonify(res.data)


@app.route('/api/songs/<string:song_id>')
def song_detail(song_id):
    song = Songs.query.get(song_id)
    res = SongsSchema().dump(song)
    return jsonify(res.data)


@app.route('/api/episodes')
def episodes_list():
    ep = Episodes.query.order_by(Episodes.date_pub).all()
    res = EpisodesSchema().dump(ep, many=True)
    return jsonify(res.data['data'])


@app.route('/api/episode/<int:episode_id>/tracklist')
def episode_tracklist(episode_id):
    ep = Episodes.query.get(episode_id)
    res = EpisodesTracklistScheam().dump(ep)
    return jsonify(res.data['data']['attributes']['tracklist']['data'])

# ----------------------------------------------------------
# Views
# ----------------------------------------------------------


@app.route('/artists')
def vw_artists_list():
    return render_template('artists.html')


@app.route('/episodes/<int:episode_id>')
def vw_episode_detail(episode_id):
    ep = Episodes.query.get(episode_id)
    res = EpisodesSchema().dump(ep).data
    return render_template('episode_detail.html', ep=res['data'])


@app.route('/')
def vw_index():
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
