import os

if os.environ.get('HOSTED') is not True:
    DEBUG = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///themetime.sqlite3'
SQLALCHEMY_TRACK_MODIFICATIONS = True
