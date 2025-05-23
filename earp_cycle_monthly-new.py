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

# TODO handle yearly compilation playlist cycling
# TODO build in args for debugging
debug = 1

if debug == 1:
    print("We're Debugging")
    ep_playlist_id = '2opAaOGzhp7txFUel5Qpic' #spotify playist ID "EP_Test"(Test)
    ep_playlist_year = '0ctAvuxTyNOrC3BRjAfOqE' #spotify yearly playlist "EP_Year"(Test)
    discord_bot_output_channel = 1309330887888080947 #discord (Test)
else:
    print("We're Live")
    ep_playlist_id = '2HPyEPDBY7NZmOV72s5rie' #spotify playist ID "Ear Porn!!(Live)"
    ep_playlist_year = '1WLV70aRmdxZbGXO9EG4oU' #spotify yearly playlist "EP_2025Collective"(Live)
    discord_bot_output_channel = 780292448298467333 #discord (Live)

sfquery = SpotipyAuthJson()
date = str(datetime.datetime.now().strftime('%Y_%m')) #var for dateyime in YYYY_MM_DD formay
year = str(datetime.datetime.now().strftime('%Y'))

ep_playlist_month = sfquery.sp.playlist(ep_playlist_id) #imports playlist as python dict
playlist_name = ep_playlist_month['name'] # var for playlist name

track_id_month = [] # store track-IDs for this cycle

discord_bot=discord_announce_v2.DiscordBot()

# File creation operations go here
app_dir=os.path.join(Path.home(), 'spotify_cycle')
output_dir=os.path.join(Path.home(), app_dir, "outputs")

try:
    os.makedirs(output_dir)
    print('Creating output directory')
except FileExistsError:
    print('Output Folder already exists.')

file_yearly_pl_csv = open((Path(output_dir)) / Path(playlist_name + '_' + date + '.csv'), 'a')


def discordAnnouncer(text):
    for part in split_multiline_string(text):
        print(part)
        discord_bot.send(discord_bot_output_channel, part)#debug discord
        #discord_bot.send(780292448298467333, part)#real discord

def cycle():
    discord_song_output="Last Month's Recap\n------------------\n" # Init the discord output with a header

    trackdata = [] # Init trackdata list
    
    file_monthly_pl_json = open((Path(output_dir)) / Path(playlist_name + '_' + date + '.json'), 'w')
    file_monthly_pl_csv = open((Path(output_dir)) / Path(playlist_name + '_' + date + '.csv'), 'a')
    file_yearly_pl_csv = open((Path(output_dir)) / Path(playlist_name + '_' + year + '.csv'), 'a')

    print(json.dumps(ep_playlist_month, indent=4) ,file=file_monthly_pl_json) #
    #discord_bot.send(1309330887888080947, 10*"YEET!\n")

    # TODO change json_to_csv_fields name to LIST
    # TODO handle choosing interesting fields better.
    # Loop through all tracks in the playlist, write interesting fields to csv
    for track in ep_playlist_month.get("tracks", {}).get("items", []):
        if track.get("track") is None:
            print("Found a track with value None")
            continue
        else:
            json_to_csv_fields = [track["track"]["name"],
                                track["track"]["album"]["name"],
                                track["track"]["album"]["artists"][0]["name"],
                                track["added_by"]["id"],
                                track["added_at"],
                                track["track"]["id"],
                                ]
        
        trackdata.append(json_to_csv_fields) #append song entry data list to trackdata dictionary
        track_id_month.append(json_to_csv_fields[-1]) #append song ID to track_id_month list for later use in moving songs between playlist
        #song data to print to discord
        discord_song_output += usernameFixer(track["added_by"]["id"]) + " - " +track["track"]["name"] + " by " + str(track["track"]["album"]["artists"][0]["name"])+"\n"
    
    #CSV Writer
    def trackwriter(filename):
        trackdata_headers = ["Track","Album","Artist","Added By","Time Added","Track ID"]
        with open(filename.name, 'a',newline="") as f:
            writer = csv.writer(f, delimiter=',')
            write_headers = not os.path.exists(filename.name) or os.path.getsize(filename.name) == 0
        
        # Write headers if the file is new or empty
            if write_headers:
                print("Writing header to new file")
                writer.writerow(trackdata_headers)

            print("Writing trackdata to " + str(filename)) 
            writer.writerows(trackdata)
    
    trackwriter(file_yearly_pl_csv)
    trackwriter(file_monthly_pl_csv)

    # Playlist manipulation logic starts here
    # Clear contents of this month's track IDs from the monthly playlist ##################
    sfquery.sp.playlist_remove_all_occurrences_of_items(ep_playlist_id, track_id_month) 
    # Write contents of this months track IDs to the yearly playlist
    sfquery.sp.playlist_add_items(ep_playlist_year, track_id_month)

    # Playlist manipulation logic ends here
    if debug == 1:
        debugCycle()

    # Announce all songs contributed by all users when cycled
    discordAnnouncer(discord_song_output)

    return(discord_song_output)

def debugCycle():
    #Adds a block of songs to the test monthly playlist for debugging.
    print("Resetting debugging playlist")
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

def addBubbleButt():
    sfquery.sp.playlist_add_items(ep_playlist_id, ['6LQAeEZ1zbZUZ5ItQI5l1b'])
    return('You did this to yourself')

def addSong(song_id):
    sfquery.sp.playlist_add_items(ep_playlist_id, [song_id])
    return('You did this to yourself')

#fuction accepts username string as parameter and converts it it matches entry in broken usernames list
def usernameFixer(username):
    brokenUsernames = [('s9o1hnuxfsrc8orhu8mdkfg1a','Adam'),
                       ('71fg5vzz2r72fuaevr48h6usr','Tré'),
                       ('xjenbeanx','Jenny'),
                       ('arshling','Jack'),
                       ('goodwi46','Aly'),
                       ('greenteakittens','Sarah'),
                       ('swbernstel','Doc'), 
                       ('krmcneil86','Keri'), 
                       ('shinditzu','Alex'),                       
                        ] 
    for i in brokenUsernames:
    #print(i)
        if i[0] in username:
            username = i[1]
    return(username)

def split_multiline_string(input_string, max_length=2000):
    """
    Splits a multiline string into parts, each less than max_length characters.
    Ensures splits occur at line breaks for better readability.
    
    Args:
        input_string (str): The input multiline string to split.
        max_length (int): The maximum length of each part (default: 2000).
    
    Returns:
        list: A list of string parts, each less than max_length characters.
    """
    if len(input_string) <= max_length:
        return [input_string]
    
    parts = []
    current_part = []

    # Track the current length of the part being built
    current_length = 0

    for line in input_string.splitlines(keepends=True):
        line_length = len(line)

        if current_length + line_length > max_length:
            # If adding this line exceeds max_length, save the current part
            parts.append(''.join(current_part))
            current_part = [line]
            current_length = line_length
        else:
            # Otherwise, add the line to the current part
            current_part.append(line)
            current_length += line_length

    # Add the last part if it contains any content
    if current_part:
        parts.append(''.join(current_part))
    
    return parts

def listContributers():
    ep_playlist_month = sfquery.sp.playlist(ep_playlist_id) #imports playlist as python dict
    userSongCount = {}
    output = ''
    un_length=0
    for track in ep_playlist_month["tracks"]["items"]:
        # userSongCount.setdefault(track["added_by"]["id"],0)
        userSongCount.setdefault(usernameFixer(track["added_by"]["id"]),0)
        userSongCount[usernameFixer(track["added_by"]["id"])] += 1

    #find value of longest username for formatting purposes
    for user in userSongCount: 
        if len(user) > un_length:
            un_length = len(user) + 1
        
    #original output style
    for user in userSongCount:
        output += user + ' contributed ' + str(userSongCount[user]) + " songs" + "\n"
    return (output)

def main():
    cycle()
    #print(usernameFixer('Alex'))
    #print(listContributers())

if __name__ == '__main__':
    main()