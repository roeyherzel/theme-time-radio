import os

if os.environ.get('DATABASE_URL') is not None:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
else:
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost/flasker'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///themetime.sqlite3'
    DEBUG = True

SQLALCHEMY_TRACK_MODIFICATIONS = True

# SERVER_NAME = "localhost:5000"
# PREFERRED_URL_SCHEME = "http"
