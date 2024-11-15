import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from pprint import pprint
from earp_auth import SpotipyAuth

sfquery = SpotipyAuth()
ep_playlist_id = '2opAaOGzhp7txFUel5Qpic' #spotify playist ID "EP_Test"
track_id_month = ['6ie0uyyvOKTTuIFBMPiNIl', 
                   '0C9u106kRYCqYSP3KDdk3v', 
                   '7jBAskQhyfjmbYC0o3pXdW', 
                   '1Jg3XdrCOZ5rrirIOggdtW', 
                   '6dU5RxthbuaN31bRbEDlNw', 
                   '0ZK8TGOsngrstVPsnrHbK1', 
                   '0iCrjwLMTjWsdOKdOAZ0FC', 
                   '3uC4r2daXertBxxc8BpbbN', 
                   '21qnJAMtzC6S5SESuqQLEK', 
                   '4efAv86uRxR4yQBcb3Vczq',
                   ]

sfquery.sp.playlist_add_items(ep_playlist_id, track_id_month)
