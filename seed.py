from archive import app
from archive.models import *

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

    def addResource(self, tag):
        resource_id = tag['id']
        res = self.resource(**self._build_query_params(tag))
        self.resource.create(res)

    def addResourceToTrack(self, tag):
        resource_id = tag['id']
        res = self.resource_to_track(self.track_id, resource_id, Status.getIdByName(self.status))
        self.resource_to_track.create(res)

    def run_querys(self, tag):
        self.addResource(tag)
        self.addResourceToTrack(tag)


class AddArtist(AddTag):
    def __init__(self, tag, track_id):
        self.tag_fields = ['id', 'name', 'thumb', 'profile', 'type', 'real_name']
        self.resource = Artists
        self.resource_to_track = TracksArtists
        super().__init__(tag, track_id)

    def addExtraInfo(self, tag):
        if tag.get('images') is not None:
            fields = ['type', 'width', 'height', 'uri', 'uri150', 'resource_url', 'artist_id']
            for img in tag['images']:
                img['artist_id'] = tag['id']
                res = ArtistsImages(**self._build_query_params(img, fields))
                ArtistsImages.create(res)

        if tag.get('aliases') is not None:
            for a in tag['aliases']:
                res = ArtistsAliases(id=a['id'], name=a['name'], artist_id=tag['id'])
                ArtistsAliases.create(res)

        if tag.get('groups') is not None:
            for a in tag['groups']:
                res = ArtistsGroups(id=a['id'], name=a['name'], artist_id=tag['id'])
                ArtistsGroups.create(res)

        if tag.get('members') is not None:
            for a in tag['members']:
                res = ArtistsMembers(id=a['id'], name=a['name'], artist_id=tag['id'])
                ArtistsMembers.create(res)

    def run_querys(self, tag):
        self.addResource(tag)
        self.addResourceToTrack(tag)
        self.addExtraInfo(tag)


class AddRelease(AddTag):
    def __init__(self, tag, track_id):
        self.tag_fields = ['id', 'title', 'thumb', 'year']
        self.resource = Releases
        self.resource_to_track = TracksReleases
        super().__init__(tag, track_id)

    def addExtraInfo(self, tag):
        if tag.get('images') is not None:
            fields = ['type', 'width', 'height', 'uri', 'uri150', 'resource_url', 'release_id']
            for img in tag['images']:
                img['release_id'] = tag['id']
                res = ReleasesImages(**self._build_query_params(img, fields))
                ReleasesImages.create(res)

        if tag.get('genres') is not None:
            for g in tag['genres']:
                res = ReleasesGenres(genre=g, release_id=tag['id'])
                ReleasesGenres.create(res)

        if tag.get('styles') is not None:
            for g in tag['styles']:
                res = ReleasesStyles(style=g, release_id=tag['id'])
                ReleasesStyles.create(res)

    def addTracklist(self, tracklist):
        tag_fields = ['id', 'position', 'title', 'type', 'duration', 'release_id']
        for tag in tracklist:
            Songs.create(Songs(**self._build_query_params(tag, tag_fields)))

    def run_querys(self, tag):
        self.addResource(tag)
        self.addResourceToTrack(tag)
        self.addExtraInfo(tag)
        self.addTracklist(tag['tracklist'])


class AddSong(AddTag):
    def __init__(self, tag, track_id):
        self.tag_fields = ['id', 'position', 'title', 'type', 'duration', 'release_id']
        self.resource = Songs
        self.resource_to_track = TracksSongs
        super().__init__(tag, track_id)


# read from json file
f = open('db.json', 'r')
json_data = json.loads(f.read())
f.close()

with app.app_context():
    db.drop_all()
    db.create_all()

    Status.create(Status(name='matched'))
    Status.create(Status(name='pending'))
    Status.create(Status(name='unmatched'))
    Status.create(Status(name='full-matched'))
    Status.create(Status(name='half-matched'))

    for ep in json_data['episodes']:  # [1:2]:

        new_episode = Episodes(id=ep['id'],
                               title=ep['title'],
                               plot=ep['plot'],
                               description=ep['description'],
                               guest=ep['guest'],
                               published=strptime(ep['published']),
                               podcast=ep['podcast_link'],
                               thumb=ep['image']['src']
                               )
        Episodes.create(new_episode)
        print("AddEpisode ({}) - {}".format(new_episode.id, ep['title']))

        for t in ep['playlist']:
            new_track = Tracks(episode_id=new_episode.id,
                               title=t['title'],
                               position=t['position'],
                               resolved=t['resolved']
                               )
            Tracks.create(new_track)

            TracksTagQuery.create(
                TracksTagQuery(
                    track_id=new_track.id,
                    song=t['query']['song'],
                    release=t['query']['release'],
                    artist=t['query']['artist']
                )
            )
            AddArtist(t['tag']['artist'], new_track.id)
            AddRelease(t['tag']['release'], new_track.id)
            AddSong(t['tag']['song'], new_track.id)
