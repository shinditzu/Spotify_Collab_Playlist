# Spotify Collab Playlist

Automated monthly cycling and tracking for a shared Spotify playlist, with Discord announcements and AI-generated commentary on each contributor's music taste.

## What it does

- **Monthly cycle**: On the first of each month, all songs are moved from a monthly collaborative playlist into a yearly archive playlist
- **CSV tracking**: Logs every song (track, artist, album, who added it, when) to yearly CSV files
- **Discord recap**: Sends a month-end summary of songs and contributors to a Discord channel
- **AI commentary**: Uses GPT-4o to generate personalized commentary about each user's musical taste
- **Discord bot**: Slash commands to query contributors and current songs

## Requirements

- Python 3.12+
- A [Spotify Developer App](https://developer.spotify.com/dashboard)
- A Discord bot token
- An OpenAI API key (for AI commentary)

## Setup

```bash
git clone https://github.com/shinditzu/Spotify_Collab_Playlist.git
cd Spotify_Collab_Playlist

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# Fill in credentials (see Configuration below)
```

### First-time Spotify auth

Run the auth script once to cache your OAuth token:

```bash
python spotiy_auth.py
```

Copy the URL it prints into a browser. After the redirect (even if it shows "connection refused"), copy the full redirect URL from the address bar and paste it back into the terminal.

## Configuration

All credentials go in `.env`:

| Variable | Description |
|---|---|
| `SPOTIPY_CLIENT_ID` | Spotify app client ID |
| `SPOTIPY_CLIENT_SECRET` | Spotify app client secret |
| `SPOTIPY_REDIRECT_URI` | OAuth redirect URI (can be a dummy URL) |
| `SPOTIFY_REFRESH_TOKEN` | Set after first auth run |
| `DISCORD_BOT_TOKEN` | Discord bot token |
| `OPENAI_API_KEY` | OpenAI API key |
| `LIVE_MONTHLY_PLAYLIST` | Spotify ID of the monthly playlist |
| `LIVE_YEARLY_PLAYLIST` | Spotify ID of the yearly archive playlist |
| `LIVE_DISCORD_CHANNEL` | Discord channel ID for announcements |
| `DEBUG_MONTHLY_PLAYLIST` | Test monthly playlist ID |
| `DEBUG_YEARLY_PLAYLIST` | Test yearly archive playlist ID |
| `DEBUG_DISCORD_CHANNEL` | Test Discord channel ID |

## Running

**Local:**

```bash
python spotify_cycle_service.py &   # Scheduler (cycles on the 1st of each month)
python discord_bot_service.py &     # Discord bot
```

**Docker:**

```bash
docker compose up --build
```

CSV outputs are written to `./outputs/`.

**Interactive CLI** (manual operations):

```bash
python spotify_tools.py
```

Options include: manual cycle, query tracks, generate AI commentary, send Discord recap.

## Discord bot commands

| Command | Description |
|---|---|
| `/hello` | Ping the bot |
| `/contributors` | List contributors and song counts |

## Project structure

```
spotiy_auth.py            # Spotify OAuth setup
spotify_tools.py          # Core playlist logic (cycling, CSV, AI commentary)
spotify_cycle_service.py  # Scheduled cycling service (runs daily at 00:15 EST)
discord_bot_service.py    # Discord bot
discord_announce_v2.py    # Discord message sender
bot_tools.py              # OpenAI integration
outputs/                  # Generated CSVs and logs
```
