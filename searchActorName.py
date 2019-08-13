from plexObjects import plex


def search_actor_name(search_term):
    search = search_term
    SEARCH = search.upper().replace(" ", "-")

    # Format results
    movie_id = ""
    search_id = ""
    results = plex.search(search)
    while movie_id == "":
        for entry in results:
            entry = str(entry)
            entry = entry.split(":")
            entry[0] = entry[0][1:]
            entry[1] = int(entry[1])
            entry[2] = entry[2][:-1]
            if entry[0] == "Movie":
                movie_id = entry[1]

    movie_roles = plex.fetchItem(movie_id).roles
    for role in movie_roles:
        role = str(role).split(":")
        actor_id = role[1]
        actor_name = role[2][:-1].upper()
        if SEARCH == actor_name:
            return actor_id
