import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from pprint import pprint
from earp_auth import SpotipyAuthJson


sfquery = SpotipyAuthJson()
#ep_playlist_id = '2opAaOGzhp7txFUel5Qpic' #spotify playist ID "EP_Test"
ep_playlist_id = '4j18cLu34moapVdi0cJkcI' #spotify playist ID "Ear Porn!(PROPER)"

track_id_month = ['6LQAeEZ1zbZUZ5ItQI5l1b']

sfquery.sp.playlist_add_items(ep_playlist_id, track_id_month)
