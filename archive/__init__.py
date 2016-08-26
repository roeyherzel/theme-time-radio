from flask import Flask, jsonify, render_template
from archive.models import db, Episodes
from archive.schemas import EpisodesSchema
from flask_restful import Api, Resource

app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)


@app.route('/episodes')
def view_episodes_list():
    ep = Episodes.query.all()
    res = EpisodesSchema().dump(ep, many=True).data
    return jsonify(res)


@app.route('/episodes/<int:episode_id>')
def view_episode(episode_id):
    ep = Episodes.query.filter_by(id=episode_id).first()
    res = EpisodesSchema().dump(ep).data
    return jsonify(res)


@app.route('/')
def hello_world():
    return render_template('index.html', name='roy', script_root="http://localhost:5000/")
