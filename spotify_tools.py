#Messing around with with info from https://spotipy.readthedocs.io/en/2.24.0/
#Also https://developer.spotify.com/documentation/web-api/concepts/scopes
# simple script to clear copy interesting fields of a collaborative playlist to CSV, clear that playlist, then
# copy all songs to a compliation playist.

import os
import json
import datetime
import csv
from pathlib import Path
import time
import dotenv
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint
from spotiy_auth import SpotipyAuth
import discord_announce_v2
import questionary
from bot_tools import ai_monthly_commentary

dotenv.load_dotenv()

def get_environment_config(use_debug=True):
    """
    Get environment configuration based on debug/live setting.
    
    Args:
        use_debug (bool): If True, use debug environment. If False, use live environment.
    
    Returns:
        dict: Configuration dictionary with playlist IDs and Discord channel
    """
    if use_debug:
        print("Using Debug Environment")
        return {
            "monthly_playlist": os.getenv("DEBUG_MONTHLY_PLAYLIST", ""),
            "yearly_playlist": os.getenv("DEBUG_YEARLY_PLAYLIST", ""),
            "discord_channel": int(os.getenv("DEBUG_DISCORD_CHANNEL", "0")),
            #"yearly_data": csv.DictReader('outputs/EP_test_2025')
        }
    else:
        print("Using Live Environment")
        return {
            "monthly_playlist": os.getenv("LIVE_MONTHLY_PLAYLIST", ""),
            "yearly_playlist": os.getenv("LIVE_YEARLY_PLAYLIST", ""),
            "discord_channel": int(os.getenv("LIVE_DISCORD_CHANNEL", "0")),
            #"yearly_data": csv.DictReader('outputs/EP_test_2025')
        }

# Get current date strings
date = datetime.datetime.now().strftime('%Y_%m')
year = datetime.datetime.now().strftime('%Y')
current_month = datetime.datetime.now().strftime('%m')

# def yearly_data_by_user(use_debug=True):
#     #config = get_environment_config(use_debug)

#     with open("outputs/Ear Porn!!_2025.csv", newline="") as yearly_csvfile:
#         reader = csv.DictReader(yearly_csvfile)
#         yearly_data = [row for row in reader]

#     # Song Dicts by User
#     user_songs = {}
#     for row in yearly_data:
#         user_id = usernameFixer(row["Added By"])
#         if user_id not in user_songs:
#             user_songs[user_id] = []
#         user_songs[user_id].append(row)

#     #pprint(user_songs.keys())
#     return user_songs

def parse_yearly_data_by_user(use_debug=True, month_filter=None):
    #config = get_environment_config(use_debug)

    with open("outputs/Ear Porn!!_2025.csv", newline="") as yearly_csvfile:
        reader = csv.DictReader(yearly_csvfile)
        if month_filter:
            track_list = [row for row in reader if row["Time Added"].startswith(f"{year}-{month_filter:02d}")]
        else:
            track_list = [row for row in reader]

    # Song Dicts by User
    user_songs = {}
    for row in track_list:
        user_id = usernameFixer(row["Added By"])
        if user_id not in user_songs:
            user_songs[user_id] = []
        else:
            user_songs[user_id].append(row)

    #pprint(user_songs.keys())
    return user_songs

def query_this_months_data_from_spotify(use_debug=True):
    sfquery = SpotipyAuth()
    config = get_environment_config(use_debug)
    ep_playlist_id = config["monthly_playlist"]
    ep_playlist_month = sfquery.get_simplified_playlist_info(ep_playlist_id)

    user_songs = {}
    for row in ep_playlist_month:
        user_id = usernameFixer(row["Added By"])
        if user_id not in user_songs:
            user_songs[user_id] = []
        else:
            user_songs[user_id].append(row)
    return user_songs


def cycle(use_debug=True, output_dir="outputs"):
    # Initialize Spotify query object
    sfquery = SpotipyAuth()
    
    # Get environment configuration
    config = get_environment_config(use_debug)
    ep_playlist_id = config["monthly_playlist"]
    ep_playlist_year = config["yearly_playlist"]
    discord_bot_output_channel = config["discord_channel"]
    
    # Validate configuration
    if not ep_playlist_id or not ep_playlist_year:
        raise ValueError("Missing required playlist IDs in environment variables")
    
    # Get playlist data
    try:
        ep_playlist_month = sfquery.get_simplified_playlist_info(ep_playlist_id)
        if not ep_playlist_month:
            raise ValueError(f"Could not access playlist: {ep_playlist_id}")
        #playlist_name = ep_playlist_month.get('name', 'Unknown_Playlist')
        playlist_name = sfquery.sp.playlist(ep_playlist_id).get('name', 'Unknown_Playlist')
    except Exception as e:
        print(f"Error accessing playlist: {e}")
        return f"Error: Could not access playlist {ep_playlist_id}"
    
    # Initialize Discord bot
    discord_bot = discord_announce_v2.DiscordBot()
    
    # Create output directory if it doesn't exist
    # Path(output_dir).mkdir(exist_ok=True)
    
    # Initialize variables
    track_id_month = []
    discord_song_output = "Last Month's Recap\n------------------\n"
    trackdata = []
    
    # Open files for writing
    # file_monthly_pl_json = open(Path(output_dir) / f"{playlist_name}_{date}.json", 'w')
    # file_monthly_pl_csv = open(Path(output_dir) / f"{playlist_name}_{date}.csv", 'a')
    file_yearly_pl_csv = open(Path(output_dir) / f"{playlist_name}_{year}.csv", 'a')
    
    try:
        # Write JSON dump
        # json.dump(ep_playlist_month, file_monthly_pl_json, indent=4)
        
        # Process tracks
        for track in ep_playlist_month:
            # if track.get("track") is None:
            #     print("Found a track with value None")
            #     continue
            
            # json_to_csv_fields = [
            #     track["track"]["name"],
            #     track["track"]["album"]["name"],
            #     track["track"]["album"]["artists"][0]["name"],
            #     track["added_by"]["id"],
            #     track["added_at"],
            #     track["track"]["id"],
            # ]
            
            #trackdata.append(track)
            track_id_month.append(track['Track ID'])
            discord_song_output += (
                f"{usernameFixer(track['Added By'])} - "
                f"{track['Track']} by "
                f"{track['Artist']}\n"
            )
        
        # Write CSV files
        try:
            _write_csv_file(file_yearly_pl_csv, trackdata)
            print(f"CSV files written successfully to {file_yearly_pl_csv.name}")
            # _write_csv_file(file_monthly_pl_csv, trackdata)
            # print(f"CSV files written successfully to {file_monthly_pl_csv.name}")
        except Exception as e:
            print(f"Error writing CSV files: {e}")
            
        # Playlist manipulation
        if track_id_month:
            sfquery.sp.playlist_remove_all_occurrences_of_items(ep_playlist_id, track_id_month)
            sfquery.sp.playlist_add_items(ep_playlist_year, track_id_month)
        
        # Debug mode specific actions
        if use_debug:
            debugCycle(ep_playlist_id, sfquery)
        
        # Send Discord announcement
        discordAnnouncer(discord_bot, discord_bot_output_channel, discord_song_output)
        
        return discord_song_output
        
    finally:
        # Clean up file handles
        # file_monthly_pl_json.close()
        #file_monthly_pl_csv.close()
        file_yearly_pl_csv.close()

def _write_csv_file(file_handle, trackdata):
    """Helper function to write CSV data with headers."""
    trackdata_headers = ["Track", "Album", "Artist", "Added By", "Time Added", "Track ID"]
    
    with open(file_handle.name, 'a', newline="") as f:
        writer = csv.writer(f, delimiter=',')
        write_headers = not os.path.exists(file_handle.name) or os.path.getsize(file_handle.name) == 0
        
        if write_headers:
            print("Writing header to new file")
            writer.writerow(trackdata_headers)
        
        print(f"Writing trackdata to {file_handle.name}")
        writer.writerows(trackdata)

def discordAnnouncer(discord_bot, discord_channel, text=''):
    """Send message to Discord channel."""
    for part in split_multiline_string(text):
        print(part)
        discord_bot.send(discord_channel, part)

def debugCycle(ep_playlist_id, sfquery):
    """Add debug tracks to the playlist."""
    print("Resetting debugging playlist")
    track_id_month = [
        '6ie0uyyvOKTTuIFBMPiNIl', '0C9u106kRYCqYSP3KDdk3v', '7jBAskQhyfjmbYC0o3pXdW',
        '1Jg3XdrCOZ5rrirIOggdtW', '6dU5RxthbuaN31bRbEDlNw', '0ZK8TGOsngrstVPsnrHbK1',
        '0iCrjwLMTjWsdOKdOAZ0FC', '3uC4r2daXertBxxc8BpbbN',
        '4efAv86uRxR4yQBcb3Vczq', '6LQAeEZ1zbZUZ5ItQI5l1b'
    ]
    time.sleep(5)
    sfquery.sp.playlist_add_items(ep_playlist_id, track_id_month)

# Keep existing utility functions unchanged
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

def listContributers(ep_playlist_id='', use_debug=False):
    """List contributors with environment support."""
    if not ep_playlist_id:
        config = get_environment_config(use_debug)
        ep_playlist_id = config["monthly_playlist"]

    sfquery = SpotipyAuth()
    ep_playlist_month = sfquery.sp.playlist(ep_playlist_id)
    
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

def addBubbleButt(ep_playlist_id='', use_debug=False):
    """Add bubble butt song with environment support."""
    if not ep_playlist_id:
        config = get_environment_config(use_debug)
        ep_playlist_id = config["monthly_playlist"]

    sfquery = SpotipyAuth()
    sfquery.sp.playlist_add_items(ep_playlist_id, ['6LQAeEZ1zbZUZ5ItQI5l1b'])
    return 'You did this to yourself'

def addSong(song_id, ep_playlist_id='', use_debug=False):
    """Add song with environment support."""
    if not ep_playlist_id:
        config = get_environment_config(use_debug)
        ep_playlist_id = config["monthly_playlist"]

    sfquery = SpotipyAuth()
    sfquery.sp.playlist_add_items(ep_playlist_id, [song_id])
    return 'You did this to yourself'

def main():

    test = SpotipyAuth()
    """Main function for direct script execution."""
    choices = ['Cycle Debug Playlist',
                'Test CSV Data',
                'Get Debug Playlist Tracks (Full)',
                'Get Debug Playlist Tracks(Interesting Fields Only)',
                'Get Live Playlist Tracks',
                'Get Live Playlist Tracks (Interesting Fields Only)',
                'Parse Yearly Data by User',
                'AI Commentary from CSV Yearly Data',
                'AI Commentary from This Month\'s Spotify Data',]
    
    selected = questionary.select(
        "Please choose an option:",
        choices=choices
    ).ask()

    if selected == 'Cycle Debug Playlist':
        cycle(use_debug=True)
    elif selected == 'Test CSV Data':
        print(parse_yearly_data_by_user(use_debug=True))
    elif selected == 'Get Debug Playlist Tracks':
        get_environment_config(use_debug=True)
        tracks = test.get_tracks_from_playlist(os.getenv("DEBUG_MONTHLY_PLAYLIST"))
        pprint(tracks)
    elif selected == 'Get Debug Playlist Tracks(Interesting Fields Only)':
        get_environment_config(use_debug=True)
        tracks = test.get_simplified_playlist_info(os.getenv("DEBUG_MONTHLY_PLAYLIST"))
        pprint(tracks)
    elif selected == 'Get Live Playlist Tracks':
        get_environment_config(use_debug=False)
        tracks = test.get_tracks_from_playlist(os.getenv("LIVE_MONTHLY_PLAYLIST"))
        pprint(tracks)
    elif selected == 'Get Live Playlist Tracks (Interesting Fields Only)':
        get_environment_config(use_debug=False)
        tracks = test.get_simplified_playlist_info(os.getenv("LIVE_MONTHLY_PLAYLIST"))
        pprint(tracks)
    elif selected == "Parse Yearly Data by User":
        choices = ['All Time', 'Filter by Month']
        selected = questionary.select(
            "Please choose an option:",
            choices=choices
        ).ask()
        if selected == 'All Time':
            user_data = parse_yearly_data_by_user(use_debug=True)
            pprint(user_data)
        elif selected == 'Filter by Month':
            month = questionary.text("Enter month (1-12):").ask()
            user_data = parse_yearly_data_by_user(use_debug=True, month_filter=int(month))
            pprint(user_data)
    elif selected == "AI Commentary from CSV Yearly Data":
        month = questionary.text("Enter month (1-12):").ask()
        user_data = parse_yearly_data_by_user(use_debug=True, month_filter=int(month))
        response=ai_monthly_commentary(user_data)
        pprint(response)
    elif selected == 'AI Commentary from This Month\'s Spotify Data': 
        get_environment_config(use_debug=False)
        user_data=test.get_simplified_playlist_info(os.getenv("LIVE_MONTHLY_PLAYLIST"))

        user_songs = {}
        for row in user_data:
            user_id = usernameFixer(row["Added By"])
            if user_id not in user_songs:
                user_songs[user_id] = []
            else:
                user_songs[user_id].append(row)

        pprint(user_songs)
        response=ai_monthly_commentary(user_songs)
        pprint(response)




if __name__ == '__main__':
    main()