from archive import app
from archive.models import db, Status, Episodes, Tracks, TracksTagQuery, TracksTagStatus, \
                                Artists, TracksArtists, Releases, TracksReleases, Songs, TracksSongs

import sqlalchemy
import json
from datetime import datetime


def strptime(timestap_list):
    timestamp_str = ' '.join([str(i) for i in timestap_list[0:6]])
    return datetime.strptime(timestamp_str, "%Y %m %d %H %M %S")


class AddTag():
    def __init__(self, tag, track_id):
        self.tag = tag
        self.status = self.tag['status']
        self.track_id = track_id
        self.name = self.__class__.__name__

        if self.status == 'unmatched':
            return None

        if type(self.tag['results']) != list:
            self.tag['results'] = [self.tag['results']]

        for tag in self.tag['results']:
            self.run_querys(tag)

    def _build_query_params(self, tag, fields=None):
        fields = fields if fields else self.tag_fields
        qp = dict([(i, tag[i]) for i in fields])
        return qp

    def add_resource(self, tag):
        resource_id = tag['id']
        res = self.class_add_resource(**self._build_query_params(tag))
        db.session.add(res)
        try:
            db.session.commit()
            print("{} ({})".format(self.name, resource_id))

        except sqlalchemy.exc.IntegrityError as err:
            db.session.rollback()
            print("WARNING - {} {}".format(err.orig.diag.message_detail, err.orig.diag.message_primary))

    def add_resource_to_track(self, tag):
        resource_id = tag['id']
        res = self.class_add_resource_to_track(self.track_id, resource_id, Status.getByName(self.status))
        db.session.add(res)
        db.session.commit()
        print("{} ({}) to track ({}) status ({})".format(self.name, resource_id, self.track_id, self.status))

    def run_querys(self, tag):
        self.add_resource(tag)
        self.add_resource_to_track(tag)


class AddArtist(AddTag):
    def __init__(self, tag, track_id):
        self.tag_fields = ['id', 'name', 'thumb', 'profile', 'type', 'real_name']
        self.class_add_resource = Artists
        self.class_add_resource_to_track = TracksArtists
        super().__init__(tag, track_id)


class AddRelease(AddTag):
    def __init__(self, tag, track_id):
        self.tag_fields = ['id', 'title', 'thumb', 'year']
        self.class_add_resource = Releases
        self.class_add_resource_to_track = TracksReleases
        super().__init__(tag, track_id)

    def add_tracklist(self, tracklist):
        tag_fields = ['id', 'position', 'title', 'type', 'duration', 'release_id']
        for tag in tracklist:
            db.session.add(Songs(**self._build_query_params(tag, tag_fields)))
            try:
                db.session.commit()
                print("TrackList: AddSong ({})".format(tag['id']))

            except sqlalchemy.exc.IntegrityError as err:
                db.session.rollback()
                print("WARNING - {} {}".format(err.orig.diag.message_detail, err.orig.diag.message_primary))

    def run_querys(self, tag):
        self.add_resource(tag)
        self.add_resource_to_track(tag)
        self.add_tracklist(tag['tracklist'])


class AddSong(AddTag):
    def __init__(self, tag, track_id):
        self.tag_fields = ['id', 'position', 'title', 'type', 'duration', 'release_id']
        self.class_add_resource = Songs
        self.class_add_resource_to_track = TracksSongs
        super().__init__(tag, track_id)


# read from json file
f = open('db.json', 'r')
json_data = json.loads(f.read())
f.close()

with app.app_context():
    db.drop_all()
    db.create_all()

    db.session.add(Status(name='matched'))
    db.session.add(Status(name='pending'))
    db.session.add(Status(name='unmatched'))
    db.session.commit()

    for ep in json_data['episodes']:  # [1:2]:

        new_episode = Episodes(id=ep['id'],
                               title=ep['title'],
                               description=ep['description'],
                               guest=ep['guest'],
                               published=strptime(ep['published']),
                               podcast=ep['link_to_listen']
                               )
        db.session.add(new_episode)
        print("AddEpisode ({}) - {}".format(new_episode.id, ep['title']))

        for t in ep['playlist']:
            new_track = Tracks(episode_id=new_episode.id,
                               title=t['title'],
                               position=t['position'],
                               resolved=t['resolved']
                               )
            db.session.add(new_track)
            db.session.commit()

            db.session.add(
                TracksTagQuery(
                            track_id=new_track.id,
                            song=t['query']['song'],
                            release=t['query']['release'],
                            artist=t['query']['artist']
                            )
            )
            db.session.commit()
            print("AddTrack ({})".format(new_track.id))

            AddArtist(t['tag']['artist'], new_track.id)
            AddRelease(t['tag']['release'], new_track.id)
            AddSong(t['tag']['song'], new_track.id)

    db.session.commit()
