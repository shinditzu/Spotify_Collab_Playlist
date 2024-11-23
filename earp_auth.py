#This is the auth module to be referenced in other scripts. This uses environment variables for the spotify
#Client ID, Client Secret and Redirect URI

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from pprint import pprint
import json
from pathlib import Path

script_dir=os.path.dirname(os.path.abspath(__file__))
token_path=os.path.join(script_dir, 'token.txt')
home_dir=Path.home()
config_file=os.path.join(home_dir, 'spotify_cycle', 'config.json')
default_config={
    "SPOTIPY_CLIENT_ID": "REPLACE_ME",
    "SPOTIPY_CLIENT_SECRET": "REPLACE_ME",
    "SPOTIPY_REDIRECT_URI": "http://localhost:8123",
    "DISCORD_BOT_TOKEN": "REPLACE_ME"
}
# Check if the configuration file exists
if not os.path.exists(config_file):
    # Create a new configuration file with default values
    with open(config_file, 'w') as file:
        json.dump(default_config, file, indent=4)
    print(f"Configuration file '{config_file}' created with default values.")
else:
    print(f"Configuration file '{config_file}' already exists.")


class SpotipyAuth:

    def __init__(self):
        """
        instantiate spotipy with my auth parameters. (uses env vars)
        """
        scope = 'user-read-private playlist-modify-public'
        client_id = os.environ.get('SPOTIPY_CLIENT_ID')
        client_secret = os.environ.get('SPOTIPY_CLIENT_SECRET')
        redirect_uri = os.environ.get('SPOTIPY_REDIRECT_URI')



        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, 
                                               client_secret=client_secret, 
                                               redirect_uri=redirect_uri,
                                               scope=scope,
                                               cache_path=token_path,
                                               open_browser=False,
                                               )
        )

class SpotipyAuthJson:
# TODO build under SpotipyAuth class and maybe trigger JSON vs ENV read via arg or something.
    def __init__(self):
        """
        instantiate spotipy with my auth parameters using JSON configuration parameters.
        """
        with open(config_file) as f:
            config = json.load(f)

        scope = 'user-read-private playlist-modify-public'
        client_id = config['SPOTIPY_CLIENT_ID']
        client_secret = config['SPOTIPY_CLIENT_SECRET']
        redirect_uri = config['SPOTIPY_REDIRECT_URI']

        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, 
                                               client_secret=client_secret, 
                                               redirect_uri=redirect_uri,
                                               scope=scope,
                                               cache_path=token_path,
                                               open_browser=False,
                                               )
        )



def main():
    test = SpotipyAuthJson()
    #pprint(test.sp.track("2S4CfxZG29GZWwDeMtBq2R"))
    pprint(test.sp.current_user())


if __name__ == '__main__':
    main()       