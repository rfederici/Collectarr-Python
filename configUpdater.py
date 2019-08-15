import yaml
import os
from searchActorName import search_actor_name
from addCollection import add_collection
from imdbGetMovies import imdb_get_movies

config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.yml')
config = yaml.load(open(config_path), Loader=yaml.FullLoader)


def config_update():
    for collection in config['collections']:
        subfilters = []

        try:
            if config['collections'][collection]['subfilters']:
                subfilters_raw = config['collections'][collection]['subfilters']
                for subfilter in subfilters_raw:
                    subfilter_string = subfilter, config['collections'][collection]['subfilters'][subfilter]
                    subfilters.append(subfilter_string)
        except:
            subfilters = None
        print("Updating collection: {collection_name}".format(collection_name=collection))
        for filter in config['collections'][collection]:
            values = str(config['collections'][collection][filter]).split(", ")
            for value in values:
                if filter == "actor":
                    data = search_actor_name(value)
                    print("Processing actor: {actor_name}...".format(actor_name=value))
                    add_collection(filter, data, collection, subfilters)
                elif filter == "imdb-list":
                    print("Gathering movies from IMDB List: {url}...".format(url=value))
                    data = imdb_get_movies(value)
                    print("Gathered movies from list, now processing...")
                    add_collection(filter, data, collection, subfilters)
            print("\n")
