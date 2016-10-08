from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event, desc, distinct
from sqlalchemy.exc import IntegrityError
from datetime import datetime

db = SQLAlchemy()

from archive.models.common import *

from archive.models.artists import *
from archive.models.albums import *
from archive.models.songs import *

from archive.models.episodes import *
from archive.models.tracks import *
