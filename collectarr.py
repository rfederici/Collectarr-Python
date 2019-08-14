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
    print("Modes: Actor(actor), IMDB List(iml), IMDB Movie Page(imp), Deletion mode(d)")
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
    elif mode == "d":
        collectName = input("Enter Collection Name: ")
        print("Searching for collection", collectName)
        results = plex.library.search(title=collectName, libtype="collection")
        if results:
            if len(results) > 1:
                selected_collection = None
                while not selected_collection:
                    print("\n")
                    print("Multiple collections found")
                    for i, result in enumerate(results):
                        print(i+1, ")", result.title)
                    choice = input("Select:")
                    try:
                        choice = int(choice)
                        if choice <= i+1 and choice > 0:
                            selected_collection = results[choice-1]
                    except:
                        print("Invalid entry")
            elif results:
                selected_collection = results[0]
            confirm = input("{} selected. Confirm deletion (y/n):".format(selected_collection.title))
            if confirm == "y":
                selected_collection.delete()
                print("Collection deleted")
                print("\n")


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
