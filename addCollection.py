from plexObjects import plex


def add_collection(method, data, name=None, subfilters=None):

    # Add collection based on actors name
    if method == "actor":
        if not name:
            search = name
        plex_actor_movies = plex.library.search(libtype="movie", actor=data)
        if plex_actor_movies:
            for movie in plex_actor_movies:
                # Search for existing collection
                plex_collections = plex.library.search(title=name, libtype="collection")
                try:
                    first_spot = plex_collections[0].children
                except:
                    first_spot = []
                if movie in first_spot:
                    print(movie.title, "is already apart of collection", name)
                else:
                    filtered = False
                    if subfilters:
                        movie_filtered = False
                        for subfilter in subfilters:
                            filter_method = subfilter[0]
                            filter_terms = str(subfilter[1]).split(", ")
                            match = False
                            for term in filter_terms:
                                if term in str(getattr(movie, filter_method)):
                                    match = True
                                else:
                                    fuck="shit"
                        if match:
                            filtered = True
                    else:
                        #add movies that didn't have subfilters applied
                        print("+++ Adding", movie.title, "to collection", name)
                        movie.addCollection(name)
                    if filtered:
                        print("+++ Adding", movie.title, "to collection", name)
                        movie.addCollection(name)


    # Add collection based on imdb list url
    elif method == 'imdb-list':
        for movie in data:
            results = plex.library.search(title=name, libtype="collection")
            try:
                first_spot = results[0].children
            except:
                first_spot = []
            if movie in first_spot:
                print(movie.title, "is already apart of collection")
            else:
                filtered = False
                if subfilters:
                    movie_filtered = False
                    for subfilter in subfilters:
                        filter_method = subfilter[0]
                        filter_terms = str(subfilter[1]).split(", ")
                        match = False
                        for filter_term in filter_terms:
                            if filter_term in str(getattr(movie, filter_method)):
                                match = True
                    if match:
                        filtered = True
                else:
                    print("+++ Adding", movie.title, "to collection", name)
                    movie.addCollection(name)
                if filtered:
                    print("+++ Adding", movie.title, "to collection", name)
                    movie.addCollection(name)

