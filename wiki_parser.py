import requests
from bs4 import BeautifulSoup
import re
from app import create_app, models

"""
    Parser for extracting all episodes from Wikipedia
    Number of Episodes: 150
    Season 1: 50
    Season 2: 25
    Season 3: 28

    * Some episodes don't have tracklist like: Episode 12 Christmas & New Year
      Resone is that those episodes are re-runs:
      "Aired December 24, 2008 as a repeat of the Season 1 episode, which was first broadcast in December 2006."
"""

prs_episode = re.compile(r"^Episode\s(?P<id>\d+):?\s(?P<title>.*?)$")

dash_list = "[{}{}{}]".format(
    b'\xe2\x80\x94'.decode(),
    b'\xe2\x80\x93'.decode(),
    '-'
)
prs_track_full = re.compile(r'^\"?(?P<song>.*?)\"?\s' + dash_list + r'\s(?P<artist>.*?)\s?\((?P<year>\d+).*?\)')
prs_track_full_loos_whitespace = re.compile(r'^\"?(?P<song>.*?)\"?\s?' + dash_list + r'\s?(?P<artist>.*?)\s?\((?P<year>\d+).*?\)')

prs_track_no_year = re.compile(r'^\"?(?P<song>.*?)\"?\s' + dash_list + r'\s(?P<artist>.*?)$')


class TrackParser(object):

    def __init__(self, track_str, position):
        self.resolved = False
        self.song, self.artist, self.year = None, None, None
        self.title = track_str
        self.position = position
        self.resolved = self.parse()

    def parse(self):
        res = prs_track_full.search(self.title)
        if not res:
            res = prs_track_full_loos_whitespace.search(self.title)
        if res:
            self.song, self.artist, self.year = res.groups()
            self.year = int('{:<04}'.format(self.year))
            return True

        res = prs_track_no_year.search(self.title)
        if res:
            self.song, self.artist = res.groups()
            return True

        print("Error...could not resolve track: {}".format(self.title.encode()))
        return False

    def dbAdd(self, episode_id):
        models.create(models.Tracks(episode_id=episode_id, resolved=self.resolved, position=self.position, title=self.title,
                                    parsed_song=self.song, parsed_artist=self.artist, year=self.year))


class EpisodeParser(object):

    def __init__(self, episode_str, aired_str, track_list):
        self.id, self.title = prs_episode.search(episode_str).groups()
        self.aired = aired_str
        self.tracklist = [TrackParser(track_list[t], t + 1) for t in range(len(track_list))]

    def dbAdd(self, season):
        new = models.Episodes(title=self.title, aired=self.aired, season=season)
        models.create(new)

        for track in self.tracklist:
            track.dbAdd(new.id)


def get_episodes_by_season(url):
    r = requests.get(url)

    if r.ok is False:
        return None

    parsed_episodes = list()
    soup = BeautifulSoup(r.content, 'html.parser')

    for ol in soup.find_all('ol'):

        if ol.has_attr("class"):
            # last ol is a reference ol
            continue

        episode_tracklist = [i.text for i in ol.findAll("li")]
        episode_header = ol.find_previous("h3")
        episode_airtime = episode_header.find_next("p")
        if episode_airtime.sup:
            episode_airtime.sup.extract()

        parsed_episodes.append(EpisodeParser(episode_header.span.text, episode_airtime.text, episode_tracklist))

    return parsed_episodes


with create_app().app_context():
    for season in [1, 2, 3]:
        url = "https://en.wikipedia.org/wiki/Theme_Time_Radio_Hour_(season_{})".format(season)
        episodes_data = get_episodes_by_season(url)

        print("=" * 50)
        print("Season {}: {} episodes".format(season, len(episodes_data)))
        print("=" * 50)
        for e in episodes_data:
            print(e.title)
            e.dbAdd(season)
