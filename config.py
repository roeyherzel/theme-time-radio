import os

DEBUG = True
# SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost/flasker'
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_TRACK_MODIFICATIONS = True
SERVER_NAME = "localhost:5000"
PREFERRED_URL_SCHEME = "http"
