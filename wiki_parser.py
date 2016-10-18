import wikipedia
import re
from pprint import pprint

from archive import app
from archive.models import *


prs_section = re.compile(r"^===\s(?P<section>.*?)\s===$")
prs_episode = re.compile(r"^Episode\s(?P<id>\d+):\s(?P<title>.*?)$")
prs_track = re.compile(r'^\"?(?P<song>.*?)\"?\s—\s(?P<artist>.*?)\s\((?P<year>\d+)\)$')


class TrackParser(object):
    def __init__(self, track, position):
        self.title = track
        self.position = position
        self.song, self.artist, self.year, self.resolved = None, None, None, False
        res = prs_track.search(self.title)
        if res:
            self.song, self.artist, self.year = res.groups()
            self.resolved = True

    def __str__(self):
        if self.resolved:
            return "<Track({}) - song:[{}] artist:[{}] year:[{}]>".format(
                self.position, self.song, self.artist, self.year
            )
        else:
            return "<Track({}) - title:[{}]>".format(self.position, self.title.encode("utf-8"))

    def props_for_db(self):
        return {
            'title': self.title,
            'song': self.song,
            'artist': self.artist,
            'position': self.position,
            'type': 'song'  # FIXME
        }


class EpisodeParser(object):
    def __init__(self, ep_section, wikiPage, tags):
        self.section = ep_section
        self.tags = tags
        self.id, self.title, self.tracklist = None, None, None
        res = prs_episode.search(ep_section)
        if res:
            self.id, self.title = res.groups()
        else:
            print("Error...parsing episode section")
            return None

        tracklist = wikiPage.section(self.section).split("\n")
        self.date_aired = tracklist.pop(0)
        self.tracklist = [TrackParser(tracklist[i], i + 1) for i in range(0, len(tracklist))]

    def __str__(self):
        return "<Episode({}) - title:[{}]>".format(self.id, self.title)

    def props_for_db(self):
        return {
            'id': self.id,
            'title': self.title,
        }


page = "Theme Time Radio Hour (season 1)"
wiki_page = wikipedia.page(page)
sections = [prs_section.findall(line)[0] for line in wiki_page.content.split("\n") if line.startswith("===")]


""" Seeding episodes & tracks to the database """
with app.app_context():
    db.drop_all()
    db.create_all()

    Status.add(Status(name='matched'))
    Status.add(Status(name='pending'))
    Status.add(Status(name='unmatched'))

    for s in sections:
        myEpisode = EpisodeParser(s, wiki_page, ["season 1"])
        print(myEpisode)
        print("=" * 100)
        newEpisode = Episodes(**myEpisode.props_for_db())
        Episodes.add(newEpisode)

        for tag in myEpisode.tags:
            EpisodesTags.add(EpisodesTags(tag=tag, episode_id=myEpisode.id))

        for myTrack in myEpisode.tracklist:
            newTrack = Tracks(episode_id=newEpisode.id, **myTrack.props_for_db())
            Tracks.add(newTrack)
