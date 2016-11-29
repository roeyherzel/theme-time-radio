from flask_script import Manager, Shell
from archive import app
from archive import models
from archive.models import db

manager = Manager(app)


@manager.command
def hello():
    print("hello")


@manager.command
def clean_db():
    models.db.drop_all()
    models.db.create_all()


@manager.command
def clean_spotify():
    models.Songs.query.delete()
    models.Albums.query.delete()
    models.Artists.query.delete()
    models.Tags.query.delete()
    models.db.session.commit()


@manager.command
def load_episodes():
    import wiki_parser
    import tth_parser


@manager.command
def load_spotify():
    from tagger import tag_all_unresolved_untagged
    tag_all_unresolved_untagged()

if __name__ == "__main__":
    manager.run()


# NOTE need to run in cli: >>> from archive.data import models
def _make_context():
    return dict(app=app, db=db, models=models)

manager = Manager(create_app)
manager.add_command("shell", Shell(make_context=_make_context))
