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

    if input("Update? (y/n): ") == "y":
        config_update()
    print("\n")
    print("Modes: Actor(actor), IMDB List(iml), IMDB Movie Page(imp), Deletion mode(d)")
    mode = input("Select Mode: ")

    if mode == "actor":
        search = input("SEARCH ACTOR NAME: ")
        plex_actor_id = search_actor_name(search)
        add_collection("actor", plex_actor_id, search)
    elif mode == "iml":
        collect_name = input("Enter Collection Name: ")
        imdb_list_id = input("Enter IMDB List ID: ")
        imdb_list_id = imdb_list_id.strip()
        imdb_movies = imdb_get_movies(imdb_list_id)
        add_collection("imdb-list", imdb_movies, collect_name)
    elif mode == "imp":
        imdb_movie_id = input("Enter IMDB Movie ID")
    elif mode == "d":
        collect_name = input("Search for Collection Name: ")
        print("Searching for collection {name}...".format(name=collect_name))
        results = plex.library.search(title=collect_name, libtype="collection")
        if results:
            if len(results) > 1:
                selected_collection = None
                while not selected_collection:
                    print("\n")
                    print("Multiple collections found")
                    for i, result in enumerate(results):
                        print("{pos}) {title}".format(pos=i+1, title=result.title))
                    choice = input("Select:")
                    try:
                        choice = int(choice)
                        if i+1 >= choice > 0:
                            selected_collection = results[choice-1]
                    except:
                        print("Invalid entry")
            elif results:
                selected_collection = results[0]
            confirm = input("{title} selected. Confirm deletion (y/n):".format(title=selected_collection.title))
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
                if len(results) >= selection > 0:
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
    print("{CHILDREN} Movies in collection".format(CHILDREN=len(result.children)))
    for movie in result.children:
        print(movie.year, "-", movie.title)


run_database_sync()
