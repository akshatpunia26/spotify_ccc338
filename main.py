import pandas as pd
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = 'dc8611201d2a4d68ac59e3623d309096'
CLIENT_SECRET = '470122036a274706a4f705ab88867fed'
REDIRECT_URI = 'https://modern-love-spotify.streamlit.app/'

client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

playlist_data = pd.read_csv('playlist_data.csv', names=['playlist_uri', 'artist', 'name', 'decade'])

st.title('Decades Playlist Generator')
st.markdown("""Select two decades from 1920 to 2010, and we'll generate a playlist of the top 20 songs from each decade!""")

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
decades = list(decades_dict.keys())

decade1 = st.selectbox('Select the first decade:', decades)
decade2 = st.selectbox('Select the second decade:', decades)

start_year1 = int(decades_dict[decade1])
end_year1 = int(start_year1) + 9
start_year2 = int(decades_dict[decade2])
end_year2 = int(start_year2) + 9

if st.button('Generate Playlist'):
    playlist1 = playlist_data[(playlist_data['decade'] == decade1) & (playlist_data['decade'] >= start_year1) & (playlist_data['decade'] <= end_year1)].sample(20)
    playlist2 = playlist_data[(playlist_data['decade'] == decade2) & (playlist_data['decade'] >= start_year2) & (playlist_data['decade'] <= end_year2)].sample(20)
    playlist = pd.concat([playlist1, playlist2]).sample(frac=1)
    playlist_name = f"{decade1} + {decade2} Playlist"
    playlist_description = f"Top 20 songs from {decade1} and {decade2}"
    playlist_tracks = playlist['playlist_uri'].tolist()
    user = sp.me()
    new_playlist = sp.user_playlist_create(user['id'], name=playlist_name, public=True, description=playlist_description)
    sp.playlist_add_items(new_playlist['id'], playlist_tracks)
    playlist_link = f"spotify:playlist:{new_playlist['id']}"
    st.markdown(f"## Your {decade1} + {decade2} Playlist")
    st.markdown(f"Check out your playlist [here]({playlist_link})!")