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

    def get_tracks_from_playlist(self, playlist_id):
        """
        Given a playlist ID, return the tracks in that playlist.
        """
        results = self.sp.playlist_items(playlist_id)
        tracks = results['items']
        while results['next']:
            results = self.sp.next(results)
            tracks.extend(results['items'])
        return tracks   
    
    def get_simplified_playlist_info(self, playlist_id):
        """
        Given a track object from Spotify API, return a simplified dictionary with key info.
        """
        playlist_tracks = self.get_tracks_from_playlist(playlist_id)
        output_list = []

        for track in playlist_tracks: 
            if track.get("track") is None:
                print("Found a track with value None")
                continue
            
            interesting_track_fields = {
                "Track":track["track"]["name"],
                "Album":track["track"]["album"]["name"],
                "Artist":track["track"]["album"]["artists"][0]["name"],
                "Added By":track["added_by"]["id"],
                "Time Added":track["added_at"],
                "Track ID":track["track"]["id"],
            }
            output_list.append(interesting_track_fields)
        return output_list
        

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
    import questionary
    test = SpotipyAuth()
    #pprint(test.sp.track("2S4CfxZG29GZWwDeMtBq2R"))

    """Main function for direct script execution."""
    choices = ['Test Auth', 
]

    selected = questionary.select(
        "Please choose an option:",
        choices=choices
    ).ask()

    if selected == 'Test Auth':
        pprint(test.sp.current_user())



if __name__ == '__main__':
    main()       