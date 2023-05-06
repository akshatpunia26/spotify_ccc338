import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify credentials
CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"
REDIRECT_URI = "http://localhost:3000"
SCOPE = "playlist-modify-private"

# Spotify authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=SCOPE))

# Decades dictionary
DECADES = {'60s': 'year:1960-1969',
           '70s': 'year:1970-1979',
           '80s': 'year:1980-1989',
           '90s': 'year:1990-1999',
           '00s': 'year:2000-2009',
           '10s': 'year:2010-2019',
           '20s': 'year:2020-2023'}

# Streamlit app
def app():
    st.set_page_config(page_title="Spotify Playlist Generator")
    st.title("Spotify Playlist Generator")

    # User inputs
    playlist_name = st.text_input("Enter a name for your playlist:")
    playlist_description = st.text_input("Enter a description for your playlist (optional):")
    decade = st.selectbox("Select a decade:", list(DECADES.keys()))
    
    if playlist_name and decade:
        year_range = DECADES[decade]
        st.write("Fetching songs from the " + decade + "...")
        results = sp.search(q=year_range, type='track', limit=50)
        tracks = results['tracks']['items']
        st.write("Songs fetched!")
        
        # Playlist creation
        user_dict = sp.me()
        playlist = sp.user_playlist_create(user_dict['id'], name=playlist_name, public=False, description=playlist_description)
        st.write(f"Playlist '{playlist_name}' created successfully!")
        
        # Adding tracks to playlist
        track_uris = [track['uri'] for track in tracks]
        sp.playlist_add_items(playlist['id'], track_uris)
        st.write(f"{len(tracks)} songs added to the playlist!")
        
# Run the app
if __name__ == '__main__':
    app()
