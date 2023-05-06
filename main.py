import pandas as pd
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API credentials
CLIENT_ID = 'dc8611201d2a4d68ac59e3623d309096'
CLIENT_SECRET = '470122036a274706a4f705ab88867fed'
REDIRECT_URI = 'https://modern-love-spotify.streamlit.app/'

# Create a Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Load the playlist data
playlist_data = pd.read_csv('playlist_data.csv')

# Set up the Streamlit app
st.title('Decades Playlist Generator')
st.markdown("""
    Select two decades from 1920 to 2010, and we'll generate a playlist of the top 20 songs from each decade!
""")

# Set up decade dictionary to handle decade ranges
decades_dict = {'1920s': '1920',
                '1930s': '1930',
                '1940s': '1940',
                '1950s': '1950',
                '1960s': '1960',
                '1970s': '1970',
                '1980s': '1980',
                '1990s': '1990',
                '2000s': '2000',
                '2010s': '2010'}

# Create a list of decades
decades = list(decades_dict.keys())

# Get user input for the decades
decade1 = st.selectbox('Select the first decade:', decades)
decade2 = st.selectbox('Select the second decade:', decades)

# Get the start and end years for each decade
start_year1 = int(decades_dict[decade1])
end_year1 = int(start_year1) + 9
start_year2 = int(decades_dict[decade2])
end_year2 = int(start_year2) + 9

# Filter the playlist data to get the top 20 songs from each decade
try:
    playlist1 = playlist_data[(playlist_data['decade'] == decade1) & (playlist_data['year'] >= start_year1) & (playlist_data['year'] <= end_year1)].sample(20)
    playlist2 = playlist_data[(playlist_data['decade'] == decade2) & (playlist_data['year'] >= start_year2) & (playlist_data['year'] <= end_year2)].sample(20)

    # Combine the playlists and shuffle the songs
    playlist = pd.concat([playlist1, playlist2]).sample(frac=1)

    # Create the Spotify playlist
    playlist_name = f"{decade1} + {decade2} Playlist"
    playlist_description = f"Top 20 songs from {decade1} and {decade2}"
    playlist_tracks = playlist['uri'].tolist()

    user = sp.me()
    playlist = sp.user_playlist_create(user['id'], name=playlist_name, public=True, description=playlist_description)
    sp.playlist_add_items(playlist['id'], playlist_tracks)

    # Display the link to the playlist
    playlist_link = f"spotify:playlist:{playlist['id']}"
    st.markdown(f"## Your {decade1} + {decade2} Playlist")
    st.markdown(f"Check out your playlist [here]({playlist_link})!")
except KeyError:
    st.error("Unable to generate playlist. Please try again.")