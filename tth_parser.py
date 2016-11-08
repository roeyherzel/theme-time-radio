import requests
import re
from bs4 import BeautifulSoup
from archive import app, models


parse_id = re.compile(r"episode-(\d+)-")
image_url_prefix = "http://www.themetimeradio.com/wp-content/uploads"
episode_url_prefix = "http://www.themetimeradio.com/episode-"
all_episodes_url = "http://www.themetimeradio.com/all/"

# build episodes url list
all_episodes_page = requests.get(all_episodes_url)
soup_all = BeautifulSoup(all_episodes_page.text, 'html.parser')
episodes_urls = [a.get('href') for a in soup_all.find_all('a') if a.get('href', '').startswith(episode_url_prefix)]
episodes_urls = dict([(int(parse_id.search(url).group(1)), url) for url in episodes_urls])

print(len(episodes_urls.keys()))


def get_episode_data(episodeObj):
    tth = requests.get(episodes_urls.get(episodeObj.id))
    soup = BeautifulSoup(tth.text, 'html.parser')
    try:
        # get image
        image = [i for i in soup.find_all('img') if image_url_prefix in i['src']][0]
        episodeObj.image = image['src']
        models.Mixin.update(episodeObj)

    except IndexError:
        pass

    # get description
    episodeObj.description = soup.p.text
    # get media
    episodeObj.media = soup.find("input", attrs={'id': 'podPressPlayerSpace_1_OrigURL'})['value']
    # update
    models.Mixin.update(episodeObj)


with app.app_context():
    for myEpisode in models.Episodes.query.order_by(models.Episodes.id).all():
        print("\n" + str(myEpisode))
        get_episode_data(myEpisode)
