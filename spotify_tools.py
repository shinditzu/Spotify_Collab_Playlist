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
import calendar

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
            "yearly_data": 'outputs/EP_test_2025.csv'
        }
    else:
        print("Using Live Environment")
        return {
            "monthly_playlist": os.getenv("LIVE_MONTHLY_PLAYLIST", ""),
            "yearly_playlist": os.getenv("LIVE_YEARLY_PLAYLIST", ""),
            "discord_channel": int(os.getenv("LIVE_DISCORD_CHANNEL", "0")),
            "yearly_data": "outputs/Ear Porn!!_2025.csv"
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

def parse_yearly_data(use_debug=True, month_filter=None):
    config = get_environment_config(use_debug)

    with open(config["yearly_data"], newline="") as yearly_csvfile:
        reader = csv.DictReader(yearly_csvfile)
        if month_filter:
            track_list = [row for row in reader if row["Time Added"].startswith(f"{year}-{month_filter:02d}")]
        else:
            track_list = [row for row in reader]
    return track_list

def parse_yearly_data_by_user(use_debug=True, month_filter=None):
    config = get_environment_config(use_debug)

    with open(config["yearly_data"], newline="") as yearly_csvfile:
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

def write_songs_to_yearly_csv(use_debug=True, output_dir="outputs"): #TODO make this work. 
    # Initialize Spotify query object
    sfquery = SpotipyAuth()
    
    # Get environment configuration
    config = get_environment_config(use_debug)
    ep_playlist_id = config["monthly_playlist"]

    
    # Validate configuration
    if not ep_playlist_id:
        raise ValueError("Missing required playlist ID in environment variables")
    
    # Get playlist data
    try:
        ep_playlist_month = sfquery.get_simplified_playlist_info(ep_playlist_id)
        if not ep_playlist_month:
            raise ValueError(f"Could not access playlist: {ep_playlist_id}")
            
        playlist_data = sfquery.sp.playlist(ep_playlist_id)
        if not playlist_data:
            raise ValueError(f"Could not retrieve playlist data for: {ep_playlist_id}")
        playlist_name = playlist_data.get('name', 'Unknown_Playlist')#Returns "Unknown_Playlist" if 'name' key is missing

    except Exception as e:
        print(f"Error accessing playlist: {e}")
        return f"Error: Could not access playlist {ep_playlist_id}"
    
    trackdata = []

    for track in ep_playlist_month:
        trackdata.append(track)

    # Open files for writing
    file_yearly_pl_csv = open(Path(output_dir) / f"{playlist_name}_{year}.csv", 'a')
    
    # Write CSV files
    _write_csv_file(file_yearly_pl_csv, trackdata)
    print(f"CSV files written successfully to {file_yearly_pl_csv.name}")


        

def cycle(use_debug=True, output_dir="outputs",write_csv=True):
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
        # ep_playlist_month = parse_yearly_data(use_debug=use_debug, month_filter=int(current_month)-1)
        if not ep_playlist_month:
            raise ValueError(f"Could not access playlist: {ep_playlist_id}")
            
        #playlist_name = ep_playlist_month.get('name', 'Unknown_Playlist')
        playlist_data = sfquery.sp.playlist(ep_playlist_id)
        if not playlist_data:
            raise ValueError(f"Could not retrieve playlist data for: {ep_playlist_id}")
        playlist_name = playlist_data.get('name', 'Unknown_Playlist')#Returns "Unknown_Playlist" if 'name' key is missing
    except Exception as e:
        print(f"Error accessing playlist: {e}")
        return f"Error: Could not access playlist {ep_playlist_id}"
    
    # Initialize Discord bot
    
    
    # Create output directory if it doesn't exist
    # Path(output_dir).mkdir(exist_ok=True)
    
    # Initialize variables
    track_id_month = []
    discord_song_output = f"**{calendar.month_name[int(current_month)]} {playlist_name} Recap**\n**------------------**\n>>> "
    
    trackdata = []
    #############
    # Open files for writing
    file_yearly_pl_csv = open(Path(output_dir) / f"{playlist_name}_{year}.csv", 'a')
    
    try:

        # Grab Track info from monthly playlist. Write to CSV and Prep discord output.
        for track in ep_playlist_month:
            
            #trackdata.append(track)
            track_id_month.append(track['Track ID'])
            discord_song_output += (
                f"{usernameFixer(track['Added By'])} - {track['Track']} by {track['Artist']}\n"
            )

    except Exception as e:
        print(f"Error accessing playlist: {e}")

        # Write CSV files
        if write_csv:
            try:
                _write_csv_file(file_yearly_pl_csv, trackdata)
                print(f"CSV files written successfully to {file_yearly_pl_csv.name}")

            except Exception as e:
                print(f"Error writing CSV files: {e}")
        elif not write_csv:
            print("Skipping CSV write as per configuration.")
    ##############
    # Playlist manipulation
    if track_id_month:
        sfquery.sp.playlist_remove_all_occurrences_of_items(ep_playlist_id, track_id_month)
        sfquery.sp.playlist_add_items(ep_playlist_year, track_id_month)
    
    # Debug mode specific actions
    if use_debug:
        debugCycle(ep_playlist_id, sfquery)
    
    # Send Basic Discord announcement
    discordAnnouncer(discord_bot_output_channel, discord_song_output)

    #Send AI generated commentary to Discord
    #AI_Commentary(use_debug, time_filter='Previous_Month')
    

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
        for track in trackdata:
            row = [track.get(header, "") for header in trackdata_headers]
            writer.writerow(row)


def discordAnnouncer(use_debug=True, text=''):
    config = get_environment_config(use_debug)
    discord_bot = discord_announce_v2.DiscordBot()
    """Send message to Discord channel."""
    for part in split_multiline_string(text):
        print(part)
        discord_bot.send(config["discord_channel"], part)

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
    
    # Check if playlist data was retrieved successfully
    if not ep_playlist_month or "tracks" not in ep_playlist_month:
        return "Error: Could not retrieve playlist data or playlist is empty"
    
    userSongCount = {}
    output = f'**{calendar.month_name[int(current_month)]} Playlist Contributors**\n**------------------**\n>>> '
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
        output += f"{user} contributed {(userSongCount[user])} songs\n"
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

def AI_Commentary(use_debug=True, time_filter='Current_Month', month=None):
    '''
    Generate AI commentary based on user data and time filter.
    Args:
        use_debug (bool): If True, use debug environment. If False, use live environment.
        time_filter (str): One of 'Year', 'Specific_Month', 'Current_Month', 'Previous_Month'.
        month (int, optional): Month (1-12) if time_filter is 'Specific_Month'.
    '''
    # Validate time_filter and month args.
    time_filter_options = ['Year', 'Specific_Month', 'Current_Month', 'Previous_Month']
    if time_filter not in time_filter_options:
        raise ValueError(f"time_filter must be one of {time_filter_options}")
    elif time_filter == 'Specific_Month' and month is None:
        raise ValueError("month must be provided when time_filter is 'Specific_Month'")
    elif time_filter == 'Specific_Month' and month is not None and (month < 1 or month > 12):
        raise ValueError("month must be between 1 and 12")

    # Get user data based on time filter
    if time_filter == 'Year':
        print("Using full year data")
        user_data = parse_yearly_data_by_user(use_debug=False)
        ai_responses=ai_monthly_commentary(user_data)

    elif time_filter == 'Specific_Month' and month is not None:
        print(f"Using specific month: {month}")
        user_data = parse_yearly_data_by_user(use_debug=False, month_filter=int(month))
        ai_responses=ai_monthly_commentary(user_data)

    elif time_filter == 'Current_Month':
        month = int(current_month)
        print(f"Using current month: {month}")
        user_data = parse_yearly_data_by_user(use_debug=False, month_filter=month)
        ai_responses=ai_monthly_commentary(user_data)

    elif time_filter == 'Previous_Month':
        month = int(current_month) - 1
        print(f"Using previous month: {month}")
        if month == 0:
            month = 12
        user_data = parse_yearly_data_by_user(use_debug=False, month_filter=month)
        ai_responses=ai_monthly_commentary(user_data)

    # Print and send AI responses to Discord
    pprint(ai_responses)
    discord_message = f"**Unsolicited AI Commentary:**\n**------------------**\n>>> Did you know that the EarPorn Bot has an AI commentary feature?"
    discordAnnouncer(use_debug, text=discord_message)

    for response in ai_responses:
        discord_message = f"**{response['name']}:**\n>>> {response['response']}**"
        discordAnnouncer(use_debug, text=discord_message)

def main():

    test = SpotipyAuth()
    """Main function for direct script execution."""
    choices = ['Cycle Debug Playlist',
                'Test CSV Data',
                'Get Debug Playlist Tracks (Full)',
                'Get Debug Playlist Tracks(Interesting Fields Only)',
                'Get Live Playlist Tracks',
                'Get Live Playlist Tracks (Interesting Fields Only)',
                'Parse Yearly Data(Live)',
                'Parse Yearly Data by User(Live)',
                'AI Commentary from CSV Yearly Data',
                'AI Commentary from This Month\'s Spotify Data',
                'write_songs_to_yearly_csv',
                'Test Discord Formatting',
                "Cycle REAL playlist(DANGER)",]
    
    selected = questionary.select(
        "Please choose an option:",
        choices=choices
    ).ask()

    if selected == 'Cycle Debug Playlist':
        cycle(use_debug=True)
    elif selected == 'Cycle REAL playlist(DANGER)':
        cycle(use_debug=False, write_csv=True)
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
    elif selected == "Parse Yearly Data(Live)":
        choices = ['All Time', 'Filter by Month']
        selected = questionary.select(
            "Please choose an option:",
            choices=choices
        ).ask()
        if selected == 'All Time':
            track_data = parse_yearly_data(use_debug=False)
            pprint(track_data)
        elif selected == 'Filter by Month':
            month = questionary.text("Enter month (1-12):").ask()
            track_data = parse_yearly_data(use_debug=False, month_filter=int(month))
            pprint(track_data)


    elif selected == "Parse Yearly Data by User(Live)":
        choices = ['All Time', 'Filter by Month']
        selected = questionary.select(
            "Please choose an option:",
            choices=choices
        ).ask()
        if selected == 'All Time':
            user_data = parse_yearly_data_by_user(use_debug=False)
            pprint(user_data)
        elif selected == 'Filter by Month':
            month = questionary.text("Enter month (1-12):").ask()
            user_data = parse_yearly_data_by_user(use_debug=False, month_filter=int(month))
            pprint(user_data)
    elif selected == "AI Commentary from CSV Yearly Data":
        choices = ['Year', 'Specific_Month', 'Current Month', 'Previous Month']
        selected = questionary.select(
            "Please choose an option:",
            choices=choices
        ).ask()
        
        if selected == 'Year':
            AI_Commentary(use_debug=False, time_filter='Year')

        elif selected == 'Specific_Month':
            month = questionary.text("Enter month (1-12):").ask()
            AI_Commentary(use_debug=False, time_filter='Specific_Month', month=int(month))

        elif selected == 'Current Month':
            AI_Commentary(use_debug=False, time_filter='Current_Month')

        elif selected == 'Previous Month':
            AI_Commentary(use_debug=False, time_filter='Previous_Month')
            
            
    elif selected == 'AI Commentary from This Month\'s Spotify Data': 
        #i dont know if i care to flesh this one out more unless i want to run it live
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
    elif selected == 'write_songs_to_yearly_csv':
        write_songs_to_yearly_csv
        write_songs_to_yearly_csv(use_debug=True)
    elif selected == 'Test Discord Formatting': 
        test_ai_responses =  [{'name': 'Tré',
                            'response': 'This user has a musical taste that is both diverse and '
                                        'nostalgic, with a mix of classic tracks and contemporary '
                                        'novelty tunes. With selections like "Moon River" by Audrey '
                                        'Hepburn and "Pretty Little Baby" by Connie Francis, they '
                                        'showcase an appreciation for timeless melodies and soulful '
                                        'performances. At the same time, tracks like "DONTTRUSTME" by '
                                        '3OH!3 and "Hiphopopotamus vs. Rhymenoceros" by Flight of the '
                                        'Conchords indicate a fondness for internet humor and playful, '
                                        'modern sounds.'},
                            {'name': 'Keri',
                            'response': "The user's music selection reveals a penchant for classic "
                                        'tracks that evoke both nostalgia and timeless appeal. By '
                                        'choosing "Dreams" by The Cranberries, they showcase an '
                                        'appreciation for 90s alternative rock with its ethereal and '
                                        'emotive sound. Additionally, "Season of the Witch" by Donovan '
                                        'highlights their taste for iconic, psychedelic influences from '
                                        'the 1960s, suggesting a fondness for music that bridges past '
                                        'eras with lasting impact.'},
                            {'name': 'Jenny',
                            'response': 'This user exhibits a penchant for ethereal and evocative music, '
                                        'as evidenced by their preference for artists such as Enya and '
                                        'Howard Shore, known for their enchanting soundscapes. '
                                        "Additionally, the selection of tracks like KALEO's stripped "
                                        "version and Rose Betts' offerings reveal an appreciation for "
                                        'soulful and expressive vocals that touch upon nostalgia and '
                                        'introspection. This taste is rounded out with a nod to the '
                                        'cinematic and atmospheric, illustrated by their interest in '
                                        'Lofi adaptations of iconic movie scores.'},
                            {'name': 'Jack',
                            'response': "Arshling's musical taste showcases a preference for electronic "
                                        'and experimental sounds, as evidenced by selections like Purity '
                                        'Ring\'s "many lives" and Whethan\'s "ENERGY." There\'s a strong '
                                        'inclination towards tracks that feature innovative production '
                                        'and modern pop elements, with artists like Weval and Jockstrap '
                                        'reflecting this contemporary and avant-garde approach. '
                                        'Furthermore, the inclusion of Kesha\'s "ATTENTION!" and '
                                        'bbno$\'s "1-800" also suggests a fondness for internet humor '
                                        'and trends, blending catchy hooks with a playful, irreverent '
                                        'style.'},
                            {'name': 'Alex',
                            'response': "The user's musical taste showcases a preference for eclectic "
                                        'and indie sounds, with a mix of both uplifting and '
                                        'introspective tracks. Artists like AJJ and Pavement suggest a '
                                        'proclivity for indie and alternative rock, while selections '
                                        'from BUSDRIVER and Remi Wolf introduce elements of experimental '
                                        'and live performance nuances. There is also an appreciation for '
                                        'singer-songwriters, as evidenced by picks from Lola Young and '
                                        'Mikayla Geier, indicating an ear for soulful and intimate '
                                        'storytelling in music.'},
                            {'name': 'Sarah',
                            'response': "The user's musical taste reflects a strong affinity for classic "
                                        'rock, with a noticeable appreciation for the timelessness and '
                                        'energy of the genre. Additionally, there is an embrace of '
                                        'soulful, nostalgic picks, highlighting a deep connection to '
                                        'music that stirs emotion and memory. This blend of classic rock '
                                        'and soulful nostalgia suggests a preference for music that both '
                                        'invigorates and soothes, tapping into the rich history of '
                                        'sound.'}]
        for response in test_ai_responses:
                discord_message = f"**AI Commentary for {response['name']}:**\n>>> {response['response']}"
                discordAnnouncer(use_debug=True, text=discord_message)


if __name__ == '__main__':
    main()