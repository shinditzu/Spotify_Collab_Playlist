clone repo to user directory
  -  git clone https://github.com/shinditzu/Spotify_Collab_Playlist.git

Set configuration values in config.json
  -  SPOTIPY_CLIENT_ID
  -  SPOTIPY_CLIENT_SECRET
  -  SPOTIPY_REDIRECT_URI
    
create venv in Spotify_Collab_Playlist directory and activate
  - python3 -m venv Spotify_Collab_Playlist/venv
  - source Spotify_Collab_Playlist/venv/bin/activate

install dependancies
  - pip install -r Spotify_Collab_Playlist/requirements.txt

Run script once from terminal to cache auth key
  - ~/Spotify_Collab_Playlist/venv/bin/python3 ~/Spotify_Collab_Playlist/earp_cycle_monthly.py
  - paste the URL provided into the terminal into a web browser, you will be redirected to whatever your redirect URI is set for.
      -  in my case its a dummy URI so I recieve "connection refused" This is fine and expected
  -  copy the URL from the address bar and paste back in to the terminal.


    

