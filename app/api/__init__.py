from flask import Flask, Blueprint
from flask_restful import Api

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

from . import podcast, spotify, tags
