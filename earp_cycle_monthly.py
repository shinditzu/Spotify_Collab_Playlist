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
from earp_auth import SpotipyAuthJson
from pathlib import Path
import os
import time
import discord_announce_v2

#print(os.environ.get('SPOTIPY_CLIENT_ID'))
#print(os.environ.get('SPOTIPY_CLIENT_SECRET'))
#TODO turn this in to a function maybe and pass playlists as args? 
# TODO handle yearly compilation playlist cycling
# TODO fix output folder permission on ubuntu
# TODO build in args for debugging
# TODO fix outputs path 

date = str(datetime.datetime.now().strftime('%Y_%m')) #var for dateyime in YYYY_MM_DD formay
ep_playlist_id = '2opAaOGzhp7txFUel5Qpic' #spotify playist ID "EP_Test"
sfquery = SpotipyAuthJson()
ep_playlist = sfquery.sp.playlist(ep_playlist_id) #imports playlist as python dict
playlist_name = ep_playlist['name'] # var for playlist name
app_dir=os.path.join(Path.home(), 'spotify_cycle')
output_dir=os.path.join(Path.home(), app_dir, "outputs")
file_monthly_pl_csv = open((Path(output_dir)) / Path(playlist_name + '_' + date + '.csv'), 'a')
track_id_month = [] # store track-IDs for this cycle
debug = 1
ep_playlist_year = '0ctAvuxTyNOrC3BRjAfOqE' #spotify yearly playlist "EP_Year"


def cycle():
    discord_song_output=""
    #ep_playlist_id = '4j18cLu34moapVdi0cJkcI+++++' #spotify playist ID "Ear Porn!(PROPER)"
    #
    trackdata = [] 
   
    home_dir=Path.home()
    script_dir=os.path.dirname(os.path.abspath(__file__))
    #output_dir=home_dir / "spotify_cycle" / "outputs"
    discord_bot=discord_announce_v2.DiscordBot()
    print(type(ep_playlist))

    # File creation operations go here
    try:
        os.makedirs(output_dir)
        print('Creating output directory')
    except FileExistsError:
        print('Output Folder already exists.')

    file_monthly_pl_json = open((Path(output_dir)) / Path(playlist_name + '_' + date + '.json'), 'w')
    file_monthly_pl_csv = open((Path(output_dir)) / Path(playlist_name + '_' + date + '.csv'), 'a')
    print(json.dumps(ep_playlist, indent=4) ,file=file_monthly_pl_json) #
    #discord_bot.send(1309330887888080947, 10*"YEET!\n")

    #TODO change json_to_csv_fields name to LIST
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
        # print("test")
        # print(json_to_csv_fields)
        
        trackdata.append(json_to_csv_fields) #append song entry data list to trackdata dictionary
        track_id_month.append(json_to_csv_fields[-1]) #append song ID to track_id_month list for later use in moving songs between playlist
        #song data to print to discord
        discord_song_output += track["added_by"]["id"] + " added " +track["track"]["name"] + " by " + track["track"]["album"]["artists"][0]["name"] + " at " + track["added_at"] + "\n"
        #print(f"{str(track["added_by"]["id"])} added {str(track["track"]["name"])} by {str(track["track"]["album"]["artists"][0]["name"])} at {str(track["added_at"])}")

    discord_bot.send(1309330887888080947, discord_song_output)#print song data to discord.

    #CSV Writer
    #TODO - this needs work. It should add headers on init.
    #pprint(type(trackdata))
    trackdata_headers = ["Track","Album","Artist","Added By","Time Added","Track ID"]
    with open(file_monthly_pl_csv.name, 'a',newline="") as f:
        writer = csv.writer(f, delimiter=',')
        write_headers = not os.path.exists(file_monthly_pl_csv.name) or os.path.getsize(file_monthly_pl_csv.name) == 0
    
    # Write headers if the file is new or empty
        if write_headers:
            writer.writerow(trackdata_headers)

        writer.writerows(trackdata)

    # Playlist manipulation logic starts here
    # clear contents of this month's track IDs from the monthly playlist
    sfquery.sp.playlist_remove_all_occurrences_of_items(ep_playlist_id, track_id_month)
    # write contents of this months track IDs to the yearly playlist
    sfquery.sp.playlist_add_items(ep_playlist_year, track_id_month)
    #print(f"{str(track["added_by"]["id"])} added {str(track["track"]["name"])} by {str(track["track"]["album"]["artists"][0]["name"])} at {str(track["added_at"])}")

    # Playlist manipulation logic ends here
    if debug == 1:
        debugCycle()

def debugCycle():
    #Adds a block of songs to the test monthly playlist for debugging.
    if debug == 1:
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
                        '6LQAeEZ1zbZUZ5ItQI5l1b',
                        ]
        time.sleep(5)
        sfquery.sp.playlist_add_items(ep_playlist_id, track_id_month)

def listContributers():
    userSongCount = {}
    output = ''
    for track in ep_playlist["tracks"]["items"]:
        userSongCount.setdefault(track["added_by"]["id"],0)
        userSongCount[track["added_by"]["id"]] += 1
    for user in userSongCount:
        output += user + ' contributed ' + str(userSongCount[user]) + " songs" + "\n"
    return (output)

def addBubbleButt():
    sfquery.sp.playlist_add_items(ep_playlist_id, ['6LQAeEZ1zbZUZ5ItQI5l1b'])
    return('You did this to yourself')

def addSong(song_id):
    sfquery.sp.playlist_add_items(ep_playlist_id, [song_id])
    return('You did this to yourself')

# def listContributers():
#     """
#     Parses a CSV file and returns unique values for the specified column.
        
#     Returns:
#         set: A set of unique values from the specified column.
#     """
#     unique_values = set()
    
#     try:
#         with open(file_monthly_pl_csv.name, mode='r', newline='', encoding='utf-8') as file:
#             reader = csv.DictReader(file)
            
#             if "Added By" not in reader.fieldnames:
#                 raise ValueError(f"Column 'Added By' does not exist in the CSV file.")
            
#             for row in reader:
#                 unique_values.add(row['Added By'])
    
#     except FileNotFoundError:
#         print(f"Error: File '{file_monthly_pl_csv}' not found.")
#     except ValueError as e:
#         print(e)
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")
    
#     return unique_values

def main():
    addBubbleButt()
    #cycle()

if __name__ == '__main__':
    main()