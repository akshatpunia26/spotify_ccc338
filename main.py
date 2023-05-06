import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify API credentials
CLIENT_ID = "dc8611201d2a4d68ac59e3623d309096"
CLIENT_SECRET = "470122036a274706a4f705ab88867fed"
REDIRECT_URI = "https://modern-love-spotify.streamlit.app/"

# Spotify scope
SCOPE = "playlist-modify-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI))

def get_track_ids_from_decades(decades):
    track_ids = []
    for decade in decades:
        year_range = f"{decade}-01-01:{decade+9}-12-31"
        results = sp.search(q=year_range, type='track', limit=50)
        for track in results['tracks']['items']:
            track_ids.append(track['id'])
    return track_ids

def create_playlist(name, description, track_ids):
    user_dict = sp.current_user()
    playlist = sp.user_playlist_create(user_dict['id'], name=name, public=False, description=description)
    sp.playlist_add_items(playlist['id'], track_ids)
    st.success("Playlist created successfully!")

def app():
    st.header("Create a Spotify Playlist")

    # Input playlist name
    playlist_name = st.text_input("Enter playlist name")

    # Input playlist description
    description = st.text_input("Enter playlist description")

    # Input decades
    decades = st.multiselect("Select decades", [i for i in range(1920, 2020, 10)])

    # Display playlist name and description
    if playlist_name and description and decades:
        track_ids = get_track_ids_from_decades(decades)
        create_playlist(playlist_name, description, track_ids)
    elif decades:
        st.warning("Please enter a playlist name and description")
    elif playlist_name or description:
        st.warning("Please select at least one decade")

if __name__ == "__main__":
    app()
