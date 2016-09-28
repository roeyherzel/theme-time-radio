from archive import app
from archive.models import *

import sqlalchemy
import json
from datetime import datetime


def strptime(timestap_list):
    timestamp_str = ' '.join([str(i) for i in timestap_list[0:6]])
    return datetime.strptime(timestamp_str, "%Y %m %d %H %M %S")


def addResourceResults(cls, resource_root, track_id):
    status = resource_root['status']
    if status == 'unmatched':
        return None

    # TODO: change discogs_tagger to always have list in results
    if type(resource_root['results']) != list:
        results = [resource_root['results']]
    else:
        results = resource_root['results']

    for tag in results:
        cls(tag, track_id, status)


class AddTag():
    def __init__(self, tag, track_id, status):
        self.tag = tag
        self.track_id = track_id
        self.status = status
        self.addResource()
        self.addResourceToTrack()

    def _build_query_params(self, tag, fields=None):
        fields = fields if fields else self.fields
        qp = dict([(i, tag[i]) for i in fields])
        return qp

    def addResource(self):
        res = self.resource(**self._build_query_params(self.tag))
        print("{} - {}".format(res, self.tag.get('thumb')))
        self.resource.add(res)

    def addResourceToTrack(self):
        res = self.resource_to_track(self.track_id, self.tag['id'], Status.getIdByName(self.status))
        self.resource_to_track.add(res)

    def getId(self):
        return self.tag['id']


class AddArtist(AddTag):
    def __init__(self, artist, track_id, status):
        self.fields = ['id', 'name', 'thumb', 'profile', 'type', 'real_name']
        self.resource = Artists
        self.resource_to_track = TracksArtists

        super().__init__(artist, track_id, status)

        if self.tag.get('urls') is not None:
            for url in self.tag.get('urls'):
                ArtistsUrls.add(ArtistsUrls(artist_id=self.tag['id'], url=url))

        if self.tag.get('images') is not None:
            fields = ['type', 'width', 'height', 'uri', 'uri150', 'resource_url', 'artist_id']
            for img in self.tag['images']:
                img['artist_id'] = self.tag['id']
                ArtistsImages.add(ArtistsImages(**self._build_query_params(img, fields)))

        if self.tag.get('aliases') is not None:
            for a in self.tag['aliases']:
                ArtistsAliases.add(ArtistsAliases(id=a['id'], name=a['name'], artist_id=self.tag['id']))

        if self.tag.get('groups') is not None:
            for a in self.tag['groups']:
                ArtistsGroups.add(ArtistsGroups(id=a['id'], name=a['name'], active=a['active'],
                                                artist_id=self.tag['id']))

        if self.tag.get('members') is not None:
            for a in self.tag['members']:
                ArtistsMembers.add(ArtistsMembers(id=a['id'], name=a['name'], active=a['active'],
                                                  artist_id=self.tag['id']))


class AddRelease(AddTag):
    def __init__(self, release, track_id, status):
        self.fields = ['id', 'title', 'thumb', 'year']
        self.resource = Releases
        self.resource_to_track = TracksReleases

        super().__init__(release, track_id, status)

        # Images
        if self.tag.get('images') is not None:
            fields = ['type', 'width', 'height', 'uri', 'uri150', 'resource_url', 'release_id']
            for img in self.tag['images']:
                img['release_id'] = self.tag['id']
                res = ReleasesImages(**self._build_query_params(img, fields))
                ReleasesImages.add(res)

        # Genres
        if self.tag.get('genres') is not None:
            for g in self.tag['genres']:
                res = ReleasesGenres(genre=g, release_id=self.tag['id'])
                ReleasesGenres.add(res)

        # Styles
        if self.tag.get('styles') is not None:
            for g in self.tag['styles']:
                res = ReleasesStyles(style=g, release_id=self.tag['id'])
                ReleasesStyles.add(res)

        # Album Songs
        fields = ['id', 'position', 'title', 'type', 'duration', 'release_id']
        for track in self.tag['tracklist']:
            Songs.add(Songs(**self._build_query_params(track, fields)))

        # Album Artists
        for artist in self.tag['artists']:
            res = AddArtist(artist, self.track_id, self.status)
            ReleasesArtists.add(ReleasesArtists(release_id=self.getId(), artist_id=res.getId()))


class AddSong(AddTag):
    def __init__(self, song, track_id, status):
        self.fields = ['id', 'position', 'title', 'type', 'duration', 'release_id']
        self.resource = Songs
        self.resource_to_track = TracksSongs

        super().__init__(song, track_id, status)


# read from json file
f = open('db.json', 'r')
json_data = json.loads(f.read())
f.close()

with app.app_context():
    db.drop_all()
    db.create_all()

    Status.add(Status(name='matched'))
    Status.add(Status(name='pending'))
    Status.add(Status(name='unmatched'))
    Status.add(Status(name='full-matched'))
    Status.add(Status(name='half-matched'))

    for ep in json_data['episodes']:    #[0:1]:

        new_episode = Episodes(id=ep['id'],
                               title=ep['title'],
                               plot=ep['plot'],
                               description=ep['description'],
                               guest=ep['guest'],
                               published=strptime(ep['published']),
                               podcast=ep['podcast_link'],
                               thumb=ep['image']['src']
                               )
        Episodes.add(new_episode)

        for cat in ep['categories']:
            EpisodesCategories.add(EpisodesCategories(category=cat, episode_id=ep['id']))

        print("AddEpisode ({}) - {}".format(new_episode.id, ep['title']))

        for track in ep['playlist']:
            new_track = Tracks(episode_id=new_episode.id,
                               title=track['title'],
                               position=track['position'],
                               resolved=track['resolved']
                               )
            Tracks.add(new_track)

            TracksTagQuery.add(
                TracksTagQuery(
                    track_id=new_track.id,
                    song=track['query']['song'],
                    release=track['query']['release'],
                    artist=track['query']['artist']
                )
            )

            addResourceResults(AddArtist, track['tag']['artist'], new_track.id)
            addResourceResults(AddRelease, track['tag']['release'], new_track.id)
            addResourceResults(AddSong, track['tag']['song'], new_track.id)
