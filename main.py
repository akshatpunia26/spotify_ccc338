import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth

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

# Set up authentication manager
auth_manager = SpotifyOAuth(
    client_id='dc8611201d2a4d68ac59e3623d309096',
    client_secret='470122036a274706a4f705ab88867fed',
    redirect_uri='https://modern-love-spotify.streamlit.app/',
    scope='playlist-modify-private,playlist-modify-public',
    cache_path='.spotipyoauthcache'
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

# Create the playlist
playlist_name = st.text_input("Enter a name for the playlist:")
description = st.text_input("Enter a description for the playlist:")
playlist = spotify.user_playlist_create(user_dict['id'], name=playlist_name, public=False, description=description)

# Get the two decades from the user
decade1 = st.selectbox("Select the first decade:", options=list(DECADES.keys()))
decade2 = st.selectbox("Select the second decade:", options=list(DECADES.keys()))

# Initialize an empty list to hold the track URIs
track_uris = []

# Search for tracks from the selected decades and add them to the list
for decade in [decade1, decade2]:
    st.write(f"Searching for {decade} songs...")
    results = spotify.search(q=f"year:{DECADES[decade]}", type="track", limit=10)
    for track in results["tracks"]["items"]:
        track_uris.append(track["uri"])
# Add the tracks to the playlist
spotify.playlist_add_items(playlist["id"], track_uris)
st.write(f"Playlist '{playlist_name}' created with {len(track_uris)} songs.")
