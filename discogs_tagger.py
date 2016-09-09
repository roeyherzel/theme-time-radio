import time
import json
import discogs_client
from discogs_client.exceptions import HTTPError


token = "WVZHgGmCtbrWFhofNchVCFGnFBqkdyWnThrWNZiW"
discogs = discogs_client.Client('ExampleApplication/0.1', user_token=token)


def tagTrack(song, release=None, artist=None):
    return Tag(song, release, artist)


def searchTag(query, *query_l, **fields):
    # To not overload the Discogs API
    time.sleep(1)
    try:
        res = discogs.search(query, **fields)

    except discogs_client.exceptions.HTTPError as err:
        print("HTTPError: {} ({})\n".format(err.msg, tag.name))
        if err.status_code == 429:
            print("Sleeping 5")
            time.sleep(5)

    if res:
        # NOTE: limiting results!!!
        return [res[r] for r in range(0, 9) if r < res.count]
    else:
        return None


class Resource():
    def __init__(self, query):
        # TODO: maybe delete those 2 attributes
        self.query = query
        self.status = 'unmatched'

    def get_tag_info(self, tag):
        pass

    def set_matched_tag(self, tag):
        self.results = self.get_tag_info(tag)
        self.status = 'matched'

    def set_pending_tags(self, pending_list):
        self.results = [self.get_tag_info(i) for i in pending_list]
        self.status = 'pending'


class Artist(Resource):
    def __init__(self, artistName):
        super().__init__(artistName)

    def get_tag_info(self, tag):
        return ArtistInfo(tag)


class Release(Resource):
    def __init__(self, releaseName):
        super().__init__(releaseName)

    def get_tag_info(self, tag):
        return ReleaseInfo(tag)

    def set_pending_tags(self, pending_list):
        """ collect top 10 match uniqe title results
            user will could manully select the correct one
        """
        uniqe_pending_list = dict()
        for p in pending_list:
            if p.title not in uniqe_pending_list:
                uniqe_pending_list[p.title] = p

        uniqe_pending_list = list(uniqe_pending_list.values())[0:9]
        super().set_pending_tags(uniqe_pending_list)


class Song(Resource):
    def __init__(self, trackName):
        super().__init__(trackName)

    def get_tag_info(self, tag):
        # NOTE: Song.get_tag_info already called from Release.get_tag_info
        return tag


class ArtistInfo():
    def __init__(self, tag):
        if tag.name == 'Various':
            print("WARNING - ignoring 'Various' artist\n")
            return None
        try:
            self.id = tag.id
            self.images = tag.images
            # TODO: collect data from data
            # self.aliases = tag.aliases
            # self.groups = tag.groups
            # self.members = tag.members
            self.name = tag.name
            self.title = tag.name
            self.profile = tag.profile
            self.real_name = tag.real_name
            self.urls = tag.urls
            self.thumb = tag.data.get('thumb')
            self.type = tag.data.get('type')

        except discogs_client.exceptions.HTTPError as err:
            print("HTTPError: {} ({})\n".format(err.msg, tag.name))
            if err.status_code == 429:
                raise Exception
            return None


class ReleaseInfo():
    def __init__(self, tag):
        self.id = tag.id
        self.genres = tag.genres
        self.artists = [ArtistInfo(i) for i in tag.artists]
        self.images = tag.images
        self.styles = tag.styles
        self.thumb = tag.thumb
        self.title = tag.title
        self.tracklist = [TrackInfo(tag.tracklist[i], i, self.id) for i in range(0, len(tag.tracklist))]
        self.year = tag.year

        self.artists = list(filter(lambda x: getattr(x, 'id', None), self.artists))


class TrackInfo():
    def __init__(self, tag, idx, release_id):
        self.id = "{}_{}".format(release_id, idx)
        self.title = tag.title
        self.release_id = release_id
        self.position = tag.position
        self.duration = tag.duration
        # self.artists = [ArtistInfo(i) for i in tag.artists]
        self.type = tag.data['type_']
        # extraartists


class Tag():
    def __init__(self, song=None, release=None, artist=None):
        self.song = Song(song)
        self.release = Release(release)
        self.artist = Artist(artist)

        if not song or not (release or artist):
            print("ERROR - cannot tag track - {}, not enogth track data\n".format(song))
            return

        # tag Artist
        if artist:
            artist_res = searchTag(artist, type='artist')
            if artist_res:
                if not self._automatic_tag('artist', artist_res):
                    self.artist.set_pending_tags(artist_res)

        # tag Release
        if release:
            if not self._query_release1(song, release, artist):
                if not self._query_release2(song, release):
                    self._query_release3(release)
        else:
            self._query_release4(song, artist)

        if self.release.status == 'matched':

            # tag Artist (from Release)
            # NOTE: seems like we havn't used that code block yet...
            if self.artist.status != 'matched':
                print("*** NOTE: artist auto tag from release\n")
                # FIXME: this is need to be fixed somehow...
                # i want only keep artist_ids on release
                # FIXME: need to check cases which there are more then 1 artist in artists
                self.artist.set_matched_tag(self.release.results.artists[0])

            # tag Song (from Release)
            if not self._automatic_tag('song', self.release.results.tracklist):
                self.song.set_pending_tags(self.release.results.tracklist)

    def __str__(self):
        track_info = dict()
        for name in ['song', 'release', 'artist']:
            resource = getattr(self, name)
            track_info[name] = resource.status

            if resource.status == 'matched':
                if name == 'artist':
                    track_info[name] += " " + resource.results.name
                else:
                    track_info[name] += " " + resource.results.title

            elif resource.status == 'pending':
                track_info[name] += "({}) ".format(len(resource.results))

        return "song   : {}\nrelease: {}\nartist : {}".format(
            track_info['song'],
            track_info['release'],
            track_info['artist']
        )

    def _automatic_tag(self, resource_name, pending_list=None):
        """verify resource query string appears in tag's title/name
           if so, call set_matched_tag
        """
        if not pending_list:
            return False

        prop = 'name' if resource_name == 'artist' else 'title'

        # must be the same ordered list we recived from discogs
        # otherwise the verification is wrong
        for tag in pending_list:
            resource = getattr(self, resource_name)
            r1 = resource.query.lower().replace('&', 'and')
            r2 = getattr(tag, prop).lower().replace('&', 'and')

            # verify match, 2-way compration now!
            if r1 in r2 or r2 in r1:
                resource.set_matched_tag(tag)
                return True

        return False

    def _query_release1(self, song, release, artist=None):
        """ 1. query release with Artist & Song
            2. automatic_tag
            3. query release with 'Various Artist' & Song
            4. automatic_tag

            * We don't try to add pending because we have all the data we need,
               so maybe data is worng
        """
        if not artist:
            return False

        # print("\tQuery1.1 - release, filter: Artist & Song")
        release_res = searchTag(release, type='release', track=song, artist=artist)

        if not self._automatic_tag('release', release_res):
            # print("\tQuery1.2 - release, filter: Various & Song")
            release_res = searchTag(release, type='release', track=song,
                                    artist='Various')

            return self._automatic_tag('release', release_res)
        else:
            return True

    def _query_release2(self, song, release):
        """ 1. query release with Song
            2. automatic tag or addPending
        """
        # print("\tQuery2 - release, filter: Song")
        release_res = searchTag(release, type='release', track=song)
        if not release_res:
            return False

        if not self._automatic_tag('release', release_res):
            self.release.set_pending_tags(release_res)
            return True

    def _query_release3(self, release):
        """ 1. query release without filters
            2. try to select-match

            * we don't try to auto-match because the song info we have
             is not specific enough
        """
        # print("\tQuery3 - release, no filter")
        release_res = searchTag(release, type='release')
        if not release_res:
            return False

        self.release.set_pending_tags(release_res)
        return True

    def _query_release4(self, song, artist=None):
        """ 1. query release with EMPTY release keyword and filter Artist & Song
            2. try to select-match

            * we don't try to auto-match because the song info we have
             is not specific enough
        """
        if not artist:
            return False

        # print("\tQuery4 - no release, filter: Artist & Song")
        release_res = searchTag('', type='release', track=song, artist=artist)
        if not release_res:
            return False

        self.release.set_pending_tags(release_res)
        return True
