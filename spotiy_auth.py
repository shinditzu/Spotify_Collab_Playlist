#This is the auth module to be referenced in other scripts. This uses environment variables for the spotify
#Client ID, Client Secret and Redirect URI

import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import os
from pprint import pprint
import json
from pathlib import Path
from dotenv import load_dotenv
from spotipy.cache_handler import MemoryCacheHandler


load_dotenv()

class SpotipyAuth:
    def __init__(self):
        """
        instantiate spotipy with my auth parameters. (uses env vars)
        """
        refresh_token = os.environ.get('SPOTIFY_REFRESH_TOKEN')
        access_token = os.environ.get('SPOTIFY_ACCESS_TOKEN')

        #print(f"Using refresh token: {refresh_token}")

        if not refresh_token:
            raise ValueError("SPOTIFY_REFRESH_TOKEN environment variable is required")

        auth_manager=SpotifyOAuth(
            client_id = os.environ.get('SPOTIPY_CLIENT_ID'),
            client_secret = os.environ.get('SPOTIPY_CLIENT_SECRET'),
            redirect_uri = os.environ.get('SPOTIPY_REDIRECT_URI'),
            scope = 'user-read-private playlist-modify-public',
            cache_handler=MemoryCacheHandler(),  # Use memory cache instead
            open_browser=False,
        )

        token_info = {
            "access_token": access_token,
            "token_type": "Bearer",
            "expires_in": 3600,
            "scope": "user-read-private playlist-modify-public",
            "expires_at": 1755142485,
            "refresh_token": refresh_token
        }

        # Set the token info in the cache handler
        auth_manager.cache_handler.save_token_to_cache(token_info)

        self.sp = spotipy.Spotify(auth_manager=auth_manager)
        

class SpotifyBotAuth:
    def __init__(self):
        # No redirect URI needed - uses client credentials only
        auth_manager = SpotifyClientCredentials(
            client_id=os.getenv('SPOTIPY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIPY_CLIENT_SECRET')
        )
        self.sp = spotipy.Spotify(auth_manager=auth_manager)

# class SpotipyAuthJson:
# # TODO build under SpotipyAuth class and maybe trigger JSON vs ENV read via arg or something.
#     def __init__(self):
#         """
#         instantiate spotipy with my auth parameters using JSON configuration parameters.
#         """

#         scope = 'user-read-private playlist-modify-public'
#         client_id = os.getenv('SPOTIPY_CLIENT_ID')
#         client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
#         redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')

#         self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, 
#                                                client_secret=client_secret, 
#                                                redirect_uri=redirect_uri,
#                                                scope=scope,
#                                                cache_path=False,
#                                                open_browser=False,
#                                                )
#         )



def main():
    test = SpotipyAuth()
    #pprint(test.sp.track("2S4CfxZG29GZWwDeMtBq2R"))
    pprint(test.sp.current_user())


    # #Test Starts here
    # ep_playlist_id = '2HPyEPDBY7NZmOV72s5rie' #spotify playist ID "Ear Porn!!(Live)"
    # sfquery = SpotipyAuthJson()
    # ep_playlist_month = sfquery.sp.playlist(ep_playlist_id) #imports playlist as python dict
    # for track in ep_playlist_month["tracks"]["items"]:
    #     json_to_csv_fields = [track["track"]["name"],
    #                         track["track"]["album"]["name"],
    #                         track["track"]["album"]["artists"][0]["name"],
    #                         track["added_by"]["id"],
    #                         track["added_at"],
    #                         track["track"]["id"],
    #                         ]
    # print(json_to_csv_fields)

if __name__ == '__main__':
    main()       