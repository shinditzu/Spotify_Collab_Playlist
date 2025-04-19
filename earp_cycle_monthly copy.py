#Messing around with with info from https://spotipy.readthedocs.io/en/2.24.0/
#Also https://developer.spotify.com/documentation/web-api/concepts/scopes
# simple scrip to clear copy interesting fields of a collaborative playlist to CSV, clear that playlist, then
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

def cycle():
    discord_song_output="""Last Month's Recap\n------------------\n
    Jenny - Orinoco Flow - 2009 Remaster by Enya
Jenny - 1,2,3,4 by Alan Doyle
Jenny - Irish Pub Song by The High Kings
Jenny - Drunken Lullabies by Flogging Molly
Jenny - City By The Sea by Dropkick Murphys
Jenny - The Donegal Lass / The Butler of Glen Avenue / Tell Me About You (feat. Luca Rapazzini) by Uncle Bard and The Dirty Bastards
Jenny - The Girl with the Red Waving Hair by The Scarlet Scallywags
Jenny - Donald Where's Your Trousers by The Irish Rovers
Adam - Body Favors by Jae Stephens
Adam - khaos theori by kaoti
Adam - LEISURE by Sam Ezeh
Adam - IF YOU GET IT YOU GET IT by Bimini
Adam - POOF BITCH by Pussy Riot
Adam - BAD BITCH by Tessa Violet
Adam - Get Outta My Way by Kylie Minogue
Adam - You Are My Religion Now by Shallowhalo
Adam - Say So Always by The Nice Device
Alex - Sound of da Police by Boogie Down Productions
Alex - Cow Killers by CHRIS CASEY
Alex - Too Happy by CHRIS CASEY
Alex - Anyone Else But You by Rubblebucket
Alex - Bugs by Jesse Welles
Alex - Bukowski - Congleton / Godbey Remix by Modest Mouse
Alex - Books for Sale by MacBook Orchestra
Alex - United Health by Jesse Welles
Alex - I Have Sex by Scoochie Boochie
Alex - Tender by Blur
Sarah - masshiro (pure white) by Fujii Kaze
Sarah - 21st Century Cool Girl by Chloe Qisha
Sarah - Fine by Lemon Demon
Sarah - The Cult of Dionysus by The Orion Experience
Sarah - Someone Who Can by Coheed and Cambria
Sarah - Stop by Spice Girls
Sarah - Living Island by Pogo
Sarah - Valentine by Laufey
Sarah - The Last Unicorn by America
Sarah - Slipping Through My Fingers by Jude York
Tré - Open Road by Ra Costelloe
Tré - emo girl (feat. WILLOW) by mgk
Tré - Larger Than Life by Backstreet Boys
Tré - Why Can't This Be Love by Van Halen
Tré - MakeDamnSure by Taking Back Sunday
Tré - Misery Business by Paramore
Tré - La Llorona by Joan Baez
Tré - Could Have Been Me by Various Artists
Doc - Slapageddon by Charles Berthoud
Doc - Mean It by Slackjaw
EXTRA LINE OF STUFF1
EXTRA LINE OF STUFF2
EXTRA LINE OF STUFF3
EXTRA LINE OF STUFF4
EXTRA LINE OF STUFF5
"""

    discord_bot=discord_announce_v2.DiscordBot()
    
    print(type(split_multiline_string(discord_song_output)))
    for part in split_multiline_string(discord_song_output):
        print(part)
        # discord_bot.send(1309330887888080947, part)#debug discord
        discord_bot.send(780292448298467333, part)#real discord
       
    # discord_bot.send(1309330887888080947, discord_song_output)#print song data to discord Debug.
    #discord_bot.send(780292448298467333, discord_song_output)#print song data to discord.

    return(discord_song_output)

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




def main():
    cycle()
    #print(usernameFixer('Alex'))
    #print(listContributers())


if __name__ == '__main__':
    main()