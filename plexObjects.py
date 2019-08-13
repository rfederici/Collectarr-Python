import os
import yaml
from plexapi.server import PlexServer

config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.yml')
config = yaml.load(open(config_path), Loader=yaml.FullLoader)

plex = PlexServer(config['server']['url'], config['server']['token'])