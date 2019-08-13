import os
import yaml
import requests
from lxml import html
from tmdbv3api import TMDb
from tmdbv3api import Movie
from plexObjects import plex

config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.yml')
config = yaml.load(open(config_path), Loader=yaml.FullLoader)

def imdb_get_movies(data):
    imdbURL = data
    movieLibrary = plex.library.section("Movies")
    library_language = plex.library.section("Movies").language
    r = requests.get(imdbURL, headers={'Accept-Language': library_language})
    tree = html.fromstring(r.content)
    title_name = tree.xpath("//div[contains(@class, 'lister-item-content')]//h3[contains(@class, 'lister-item-header')]//a/text()")
    title_years = tree.xpath("//div[contains(@class, 'lister-item-content')]//h3[contains(@class, 'lister-item-header')]//span[contains(@class, 'lister-item-year')]/text()")
    title_ids = tree.xpath("//div[contains(@class, 'lister-item-image')]//a/img//@data-tconst")
    tmdb = TMDb()
    tmdb.api_key = config['tmdb']['apikey']
    movie = Movie()
    imdb_map = {}
    matchedMovies = []
    for m in plex.library.section("Movies").all():
        if 'themoviedb://' in m.guid:
            if not tmdb.api_key == "None":
                tmdb_id = m.guid.split('themoviedb://')[1].split('?')[0]
                tmdbapi = movie.details(tmdb_id)
                imdb_id = tmdbapi.imdb_id
            else:
                imdb_id = None
        elif 'imdb://' in m.guid:
            imdb_id = m.guid.split('imdb://')[1].split('?')[0]
        else:
            imdb_id = None

        if imdb_id and imdb_id in title_ids:
            imdb_map[imdb_id] = m
        else:
            imdb_map[m.ratingKey] = m
        if imdb_id in title_ids:
            matchedMovies.append(m)
    return matchedMovies
