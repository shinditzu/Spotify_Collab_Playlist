#Messing around with with info from https://spotipy.readthedocs.io/en/2.24.0/
#Also https://developer.spotify.com/documentation/web-api/concepts/scopes
# simple script to clear copy interesting fields of a collaborative playlist to CSV, clear that playlist, then
# copy all songs to a compliation playist.

from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint
import json
import datetime
import csv
from earp_auth import SpotipyAuth
from pathlib import Path
import os
import time

#print(os.environ.get('SPOTIPY_CLIENT_ID'))
#print(os.environ.get('SPOTIPY_CLIENT_SECRET'))
#TODO turn this in to a function maybe and pass playlists as args? 
# TODO handle yearly compilation playlist cycling
# TODO fix output folder permission on ubuntu
# TODO build in args for debugging

sfquery = SpotipyAuth()
date = str(datetime.datetime.now().strftime('%Y_%m')) #var for dateyime in YYYY_MM_DD formay
ep_playlist_id = '2opAaOGzhp7txFUel5Qpic' #spotify playist ID "EP_Test"
#ep_playlist_id = '4j18cLu34moapVdi0cJkcI+++++' #spotify playist ID "Ear Porn!(PROPER)"
ep_playlist_year = '7MxI1FJA86x3FP05bXMORa' #spotify yearly playlist "EP_Year"
ep_playlist = sfquery.sp.playlist(ep_playlist_id) #imports playlist as python dict
playlist_name = ep_playlist['name'] # var for playlist name
#trackdata_headers = ["Track","Album","Artist","Added By","Time Added","Track ID"]
trackdata = []
track_id_month = []
debug = 1
script_dir=os.path.dirname(os.path.abspath(__file__))
output_dir=os.path.join(script_dir, '/output')
#token_path=os.path.join(script_dir, "token.txt")

# File creation operations go here
try:
    os.makedirs('./outputs')
except FileExistsError:
    print('Folder already exists.')

file_monthly_pl_json = open((Path('outputs')) / Path(playlist_name + '_' + date + '.json'), 'w')
#file_monthly_pl_json = open(playlist_name + '_' + date + '.json', 'w')
file_monthly_pl_csv = open((Path('outputs')) / Path(playlist_name + '_' + date + '.csv'), 'a')
#file_monthly_pl_csv = open(playlist_name + '_' + date + '.csv', 'r')

print(json.dumps(ep_playlist, indent=4) ,file=file_monthly_pl_json) #

# TODO handle choosing interesting fields better.
#Loop through all tracks in the playlist, write interesting fields to csv
for track in ep_playlist["tracks"]["items"]:
    json_to_csv_fields = [track["track"]["name"],
                          track["track"]["album"]["name"],
                          track["track"]["album"]["artists"][0]["name"],
                          track["added_by"]["id"],
                          track["added_at"],
                          track["track"]["id"],
                          ]
    trackdata.append(json_to_csv_fields)
    track_id_month.append(json_to_csv_fields[-1])
    #print(df)
    #print(json_to_csv_fields)

#CSV Writer
#TODO - this needs work. It should add headers on init.
with open(file_monthly_pl_csv.name, 'a',newline="") as f:
    writer = csv.writer(f, delimiter=',')
    #writer.writerow(trackdata_headers)
    writer.writerows(trackdata)

""" with open(file_monthly_pl_csv.name, 'a',newline="") as f:
    writer = csv.DictWriter
    #writer.writerow(trackdata_headers)
    writer.writerows(trackdata) """

print(track_id_month)

# Playlist manipulation logic starts here
# clear contents of this months track IDs to the monthly playlist
sfquery.sp.playlist_remove_all_occurrences_of_items(ep_playlist_id, track_id_month)
# write contents of this months track IDs to the yearly playlist
sfquery.sp.playlist_add_items(ep_playlist_year, track_id_month)
# Playlist manipulation logic ends here

#Adds a block of songs to the monthly playlist for debugging.
if debug == 1:
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
    time.sleep(5)
    sfquery.sp.playlist_add_items(ep_playlist_id, track_id_month)
