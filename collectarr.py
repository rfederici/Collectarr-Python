import os
import sys
import json
import requests
import time
import platform
import plexapi
import yaml
from lxml import html
from plexapi.server import PlexServer
from tmdbv3api import TMDb
from tmdbv3api import Movie

# Start with a nice clean screen
os.system('cls' if os.name == 'nt' else 'clear')

# Hacky solution for Python 2.x & 3.x compatibility
if hasattr(__builtins__, 'raw_input'):
    input=raw_input


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
	try:
		plex = PlexServer(PLEX_URL, PLEX_TOKEN)
	except:
		print("Error connecting to Plex Server")
		input("Press Enter to exit")
		sys.exit()

	def searchActorName(searchTerm):
		search = searchTerm
		SEARCH = search.upper().replace(" ", "-")
		
		#Format results
		movieID = "" 
		searchID = ""
		results = plex.search(search)
		while movieID == "":
			for entry in results:
				entry = str(entry)
				entry = entry.split(":")
				entry[0] = entry[0][1:]
				entry[1] = int(entry[1])
				entry[2] = entry[2][:-1]
				if entry[0] == "Movie":
					movieID = entry[1]
		
		movieRoles = plex.fetchItem(movieID).roles
		for role in movieRoles:
			role = str(role).split(":")
			actorID = role[1]
			actorName = role[2][:-1].upper()
			if SEARCH == actorName:
				return actorID

	def imdbGetMovies(title, data):
		collection_title = title
		imdbURL = data
		movieLibrary = plex.library.section("Movies")
		library_language = plex.library.section("Movies").language
		r = requests.get(imdbURL, headers={'Accept-Language': library_language})
		tree = html.fromstring(r.content)
		title_name = tree.xpath("//div[contains(@class, 'lister-item-content')]//h3[contains(@class, 'lister-item-header')]//a/text()")
		title_years = tree.xpath("//div[contains(@class, 'lister-item-content')]//h3[contains(@class, 'lister-item-header')]//span[contains(@class, 'lister-item-year')]/text()")
		title_ids = tree.xpath("//div[contains(@class, 'lister-item-image')]//a/img//@data-tconst")
		tmdb = TMDb()
		tmdb.api_key = parser.get('tmdb', 'apikey')
		movie = Movie()
		imdb_map = {}
		matchedMovies = []
		for m in plex.library.section("Movies").all():
			if 'themoviedb://' in m.guid:
				if tmdb.api_key:
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



	def addCollection(method, data, name=""):

		#Add collection based on actors name
		if method == "actor-name":
			plexActorMovies = plex.library.search(libtype="movie", actor=data)
			if plexActorMovies:
				for movie in plexActorMovies:
					collections = movie.collections
					collectionNames = []
					for collection in collections:
						collectionName = str(collection).split(":")
						collectionName = collectionName[1][:-1].upper()
						collectionNames.append(collectionName)
					if not search.upper().replace(" ", "-") in collectionNames:
						print "+++ Adding", movie.title, "to collection"
						movie.addCollection(search)
					else:
						print movie.title, "already apart of collection"
		elif method == 'imdb-list':
			results = plex.library.search(title=name, libtype="collection")
			firstSpot = results[0].title
			for movie in data:
				if name.upper() == firstSpot.upper() and movie in results[0].children:
						print movie.title, "already apart of collection"
				else:
						movie.addCollection(name)
						print "+++ Adding", movie.title, "to collection"

	print("Modes: Actor(actor), IMDB List(iml), IMDB Movie Page(imp)")
	mode = input("Select Mode: ")

	if mode == "actor":
		search = input("SEARCH ACTOR NAME: ")
		plexActorID = searchActorName(search)
		addCollection("actor-name", plexActorID)
	elif mode == "iml":
		collectName = input("Enter Collection Name: ")
		imdbListID= input("Enter IMDB List ID: ")
		imdbMovies = imdbGetMovies(collectName, imdbListID)
		addCollection("imdb-list", imdbMovies, collectName)
	elif mode == "imp":
		imdbMovieID = input("Enter IMDB Movie ID")
			

	#Search for existing collection 
	search = input("Enter Collection Name: ")
	results = plex.library.search(title=search, libtype="collection")
	
	if len(results) > 1:
		selection = ""
		while selection != "valid":	
			i = 1
			for result in results:
				print "{POS}) {TITLE} - {RATINGKEY}".format(POS=i, TITLE=result.title, RATINGKEY=result.ratingKey)
				i+=1	
			selection = input("Select collections (N for None): ")
			try:
				selection = int(selection)
				if selection <= len(results) and selection > 0:
					result = results[selection - 1]
					selection = "valid"
			except:
				if selection == "N":
					print "Do This Later"
					sys.exit()
	elif len(results) == 1:
		print "Found {TITLE} - {RATINGKEY}".format(TITLE=results[0].title, RATINGKEY=results[0].ratingKey)
		result = results[0]
	else:		
		yn = input("Collection does not exist. Would you like to add it? (y/n): ")
		if yn.upper() == "Y":
			print "DO THIS LATER"
			sys.exit()
		else:
			sys.exit()
	movieCount = len(result.children)
	print("{CHILDREN} Movies in collection".format(CHILDREN=movieCount))
	for movie in result.children:
		print(movie.year, "-", movie.title)
run_database_sync()
