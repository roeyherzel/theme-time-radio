from flask_script import Manager, Shell
from app import create_app
from app.models import *

manager = Manager(create_app())


@manager.command
def hello():
    print("hello")


@manager.command
def create():
    db.drop_all()
    db.create_all()


@manager.command
def addEpisodes():
    import wiki_parser
    import tth_parser


@manager.command
def addMusic():
    from music_tagger import tag_all_unresolved_untagged
    tag_all_unresolved_untagged()


@manager.command
def scrubGenres():
    # Delete Genres with less then artists
    sq = db.session.query(aux_artists_tags.c.tag_id) \
                   .join(Tags, Tags.id == aux_artists_tags.c.tag_id) \
                   .group_by(aux_artists_tags.c.tag_id) \
                   .having(func.count(aux_artists_tags.c.artist_id) < 5) \
                   .subquery()

    db.session.query(aux_artists_tags).filter(aux_artists_tags.c.tag_id.in_(sq)).delete(synchronize_session=False)

    # Delete empty Genres
    sq = db.session.query(aux_artists_tags.c.tag_id).subquery()
    Tags.query.filter(~Tags.id.in_(sq)).delete(synchronize_session=False)

    # Commit delete
    db.session.commit()

    # Show states
    stats = db.session.query(aux_artists_tags.c.tag_id, Tags.name, func.count(aux_artists_tags.c.artist_id)) \
                      .join(Tags, Tags.id == aux_artists_tags.c.tag_id) \
                      .group_by(aux_artists_tags.c.tag_id) \
                      .order_by(func.count(aux_artists_tags.c.artist_id))

    for id, name, count in stats:
        print("{} - {} ({})".format(count, name, id))

if __name__ == "__main__":
    manager.run()


def _make_context():
    return dict(app=app, db=db, models=models)

manager = Manager(create_app)
manager.add_command("shell", Shell(make_context=_make_context))
