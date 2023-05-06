import streamlit as st
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Set up authentication manager
CLIENT_ID = 'dc8611201d2a4d68ac59e3623d309096'
CLIENT_SECRET = '470122036a274706a4f705ab88867fed'
REDIRECT_URI = 'https://modern-love-spotify.streamlit.app/'
SCOPE = 'playlist-modify-private,playlist-modify-public'
CACHE_PATH = '.spotipyoauthcache'

auth_manager = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE,
    cache_path=CACHE_PATH,
)

# Get access token
access_token = None
try:
    token_info = auth_manager.get_cached_token()
    if token_info:
        access_token = token_info['access_token']
except:
    pass

if not access_token:
    auth_url = auth_manager.get_authorize_url()
    st.write('Please visit this URL to authorize the application:', auth_url)
    response = st.experimental_get_query_params()
    if 'code' in response:
        auth_code = response['code'][0]
        token_info = auth_manager.get_access_token(auth_code)
        access_token = token_info['access_token']
    else:
        st.stop()

# Use access token to get current user
spotify = spotipy.Spotify(auth=access_token)
user_dict = spotify.current_user()

# Define the available decades
DECADES = {
    "1920s": "1920-1929",
    "1930s": "1930-1939",
    "1940s": "1940-1949",
    "1950s": "1950-1959",
    "1960s": "1960-1969",
    "1970s": "1970-1979",
    "1980s": "1980-1989",
    "1990s": "1990-1999",
    "2000s": "2000-2009",
    "2010s": "2010-2019",
}

# Initialize the Spotipy client with the OAuth flow
sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="playlist-modify-private,playlist-modify-public",
    cache_path=".spotifycache",
)

# Get the user's access token
access_token = None
token_info = sp_oauth.get_cached_token()
if token_info and sp_oauth.is_token_valid(token_info):
    access_token = token_info["access_token"]
if not access_token:
    auth_url = sp_oauth.get_authorize_url()
    st.write("Please visit this URL to authorize the application:", auth_url)
    response = st.experimental_get_query_params()
    code = response["code"]
    token_info = sp_oauth.get_access_token(code)
    access_token = token_info["access_token"]

# Initialize the Spotipy client with the user's access token
sp = spotipy.Spotify(auth=access_token)

# Create the playlist
playlist_name = st.text_input("Enter a name for the playlist:")
description = st.text_input("Enter a description for the playlist:")
playlist = sp.user_playlist_create(user=sp.current_user()["id"], name=playlist_name, public=False, description=description)

# Initialize an empty list to hold the track URIs
track_uris = []

# Iterate over the decades and search for tracks
for decade, year_range in DECADES.items():
    st.write(f"Searching for {decade} songs...")
    results = sp.search(q=f"year:{year_range}", type="track", limit=10)
    for track in results["tracks"]["items"]:
        track_uris.append(track["uri"])
        st.write(f"{track['name']} by {track['artists'][0]['name']} ({decade}) - {track['external_urls']['spotify']}")

# Add the tracks to the playlist
sp.playlist_add_items(playlist["id"], track_uris)
st.write(f"Playlist '{playlist_name}' created with {len(track_uris)} songs.")

