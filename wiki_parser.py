import wikipedia
import re
from pprint import pprint

from archive import app, models


prs_section = re.compile(r"^===\s(?P<section>.*?)\s===$")
prs_episode = re.compile(r"^Episode\s(?P<id>\d+):\s(?P<title>.*?)$")
prs_track = re.compile(r'^\"?(?P<song>.*?)\"?\s—\s(?P<artist>.*?)\s\((?P<year>\d+)\)$')


class TrackParser(object):
    def __init__(self, track, position):
        self.title = track
        self.position = position
        self.song, self.artist, self.year, self.tags = None, None, None, None
        self.resolved = False
        res = prs_track.search(self.title)
        if res:
            self.song, self.artist, self.year = res.groups()
            self.resolved = True
            self.tags = [self.year]

    def __str__(self):
        if self.resolved:
            return "<Track({}) - song:[{}] artist:[{}] year:[{}]>".format(
                self.position, self.song, self.artist, self.year
            )
        else:
            return "<Track({}) - title:[{}]>".format(self.position, self.title.encode("utf-8"))

    def dict(self):
        return {
            'title': self.title, 'parsed_song': self.song, 'parsed_artist': self.artist,
            'position': self.position, 'resolved': self.resolved,
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

    def dict(self):
        return {'id': self.id, 'title': self.title}


page = "Theme Time Radio Hour (season 1)"
wiki_page = wikipedia.page(page)
sections = [prs_section.findall(line)[0] for line in wiki_page.content.split("\n") if line.startswith("===")]


""" Seeding episodes & tracks to the database """
with app.app_context():
    models.db.drop_all()
    models.db.create_all()

    for section in sections:
        parsedEpisode = EpisodeParser(section, wiki_page, ["season 1"])
        print(parsedEpisode)
        print("=" * 100)
        newEpisode = models.Episodes(**parsedEpisode.dict())
        models.Episodes.add(newEpisode, tags=parsedEpisode.tags)

        for parsedTrack in parsedEpisode.tracklist:
            newTrack = models.Tracks(episode_id=newEpisode.id, **parsedTrack.dict())
            models.Tracks.add(newTrack, tags=parsedTrack.tags)
