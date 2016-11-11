
from flask import Flask
app = Flask(__name__)
app.config.from_object('config')

from archive.models import db
db.init_app(app)

from flask_restful import Api
api = Api(app)

import archive.resources.podcast
import archive.resources.spotify
import archive.resources.tags
import archive.views
