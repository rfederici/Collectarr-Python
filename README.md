Usage: python collectarr.py

Edit config.yml with your plex server details. Modify collections as needed. Only two main filters that are working currently are actor and imdb-list, a bunch of subfilters should work such as year, genres, studio but not all have been tested.

Bugs:

subfitlers are supposed to work by only allowing a movie through if they satisfy at least one value per key (for example year = 2009). Currently it is allowing movies to go through by having at least one match on any subfilter
