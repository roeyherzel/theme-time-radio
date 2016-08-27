from flask import Flask, jsonify, render_template
from archive.models import *
from archive.schemas import *
from flask_restful import Api, Resource

app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)


@app.route('/api/artists')
def view_artists_list():
    ep = Artists.query.join(TracksArtists, (TracksArtists.artist_id == Artists.id)) \
                      .filter(TracksArtists.status == Status.getByName('matched')).order_by(Artists.name).all()
    res = ArtistsSchema().dump(ep, many=True).data
    return jsonify(res)


@app.route('/api/episodes')
def view_episodes_list():
    ep = Episodes.query.order_by(Episodes.date_pub).all()
    res = EpisodesSchema().dump(ep, many=True).data
    return jsonify(res)


@app.route('/api/episodes/<int:episode_id>')
def view_episode(episode_id):
    ep = Episodes.query.filter_by(id=episode_id).first()
    res = EpisodesSchema().dump(ep).data
    return jsonify(res)


@app.route('/artists')
def view_artists():
    return render_template('show_artists.html')


@app.route('/')
def view_episodes():
    return render_template('show_episodes.html', script_root="http://localhost:5000/")
