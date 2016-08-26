from flask import Flask, jsonify
from archive.models import db, Episodes, EpisodesSchema
from flask_restful import Api, Resource

app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)


@app.route('/episodes')
def view_episodes_list():
    ep = Episode.query.all()
    res = EpisodeSchema().dump(ep, many=True).data
    return jsonify(res)


@app.route('/episodes/<int:episode_id>')
def view_episode(episode_id):
    ep = Episode.query.filter_by(id=episode_id).first()
    res = EpisodeSchema().dump(ep).data
    return jsonify(res)


@app.route('/')
def hello_world():
    return 'Hello, World!'
