import os
import sys
import yaml
from plexObjects import plex
from configUpdater import config_update
from searchActorName import search_actor_name
from addCollection import add_collection
from imdbGetMovies import imdb_get_movies


# Start with a nice clean screen
os.system('cls' if os.name == 'nt' else 'clear')

# Hacky solution for Python 2.x & 3.x compatibility
if hasattr(__builtins__, 'raw_input'):
    input = raw_input

### Header ###
print("===================================================================")
print(" Python Plex Collections by /u/iRawrz  ")
print("===================================================================")
print("\n")

# Process config.yml
config = yaml.load(open('config.yml'), Loader=yaml.FullLoader)
PLEX_URL = config['server']['url']
PLEX_TOKEN = config['server']['token']
PLEX_LIBRARIES = config['server']['library'].split(',')


def run_database_sync():

    if (input("Update? (y/n): ") == "y"):
        config_update()
    print("\n")
    print("Modes: Actor(actor), IMDB List(iml), IMDB Movie Page(imp)")
    mode = input("Select Mode: ")

    if mode == "actor":
        search = input("SEARCH ACTOR NAME: ")
        plexActorID = search_actor_name(search)
        add_collection("actor", plexActorID, search)
    elif mode == "iml":
        collectName = input("Enter Collection Name: ")
        imdbListID = input("Enter IMDB List ID: ")
        imdbListID = imdbListID.strip()
        imdbMovies = imdb_get_movies(imdbListID)
        add_collection("imdb-list", imdbMovies, collectName)
    elif mode == "imp":
        imdbMovieID = input("Enter IMDB Movie ID")

    # Search for existing collection
    search = input("Enter Collection Name: ")
    results = plex.library.search(title=search, libtype="collection")

    if len(results) > 1:
        selection = ""
        while selection != "valid":
            i = 1
            for result in results:
                print("{POS}) {TITLE} - {RATINGKEY}".format(POS=i, TITLE=result.title, RATINGKEY=result.ratingKey))
                i += 1
            selection = input("Select collections (N for None): ")
            try:
                selection = int(selection)
                if selection <= len(results) and selection > 0:
                    result = results[selection - 1]
                    selection = "valid"
            except:
                if selection == "N":
                    print("Do This Later")
                    sys.exit()
    elif len(results) == 1:
        print("Found {TITLE} - {RATINGKEY}".format(TITLE=results[0].title, RATINGKEY=results[0].ratingKey))
        result = results[0]
    else:
        yn = input("Collection does not exist. Would you like to add it? (y/n): ")
        if yn.upper() == "Y":
            print("DO THIS LATER")
            sys.exit()
        else:
            sys.exit()
    movieCount = len(result.children)
    print("{CHILDREN} Movies in collection".format(CHILDREN=movieCount))
    for movie in result.children:
        print(movie.year, "-", movie.title)


run_database_sync()
