import streamlit as st
import spotipy
from spotipy.outh2 import SpotifyClientCredentials

client_id = '37399f78d90b404d8d20de02f1ef6886'
client_secret = 'e400332f962e4838b57fb35c710ecc01'
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

decades = {'1920s': 'https://open.spotify.com/playlist/7HWmbcjkVTfQdLKk2NWmtZ?si=6b870f33efe24872' ,
           '1930s': 'https://open.spotify.com/playlist/2webFRRyZuTUdw9KrMKT63?si=08ee3c375cba4319' ,
           '1940s': 'https://open.spotify.com/playlist/1KTSHAsbCgSnZLMdXp52Ln?si=93366e637d9349ca' ,
           '1950s': 'https://open.spotify.com/playlist/431BefAztO1PGCR4yd6PXL?si=231a737083dc4906',
            '1960s': 'https://open.spotify.com/playlist/37i9dQZF1DWYUCqLrWKr4p?si=9231af5a094b4d58',
            '1970s': 'https://open.spotify.com/playlist/37i9dQZF1DWY373eEGlSj4?si=02b1f17f991141c3',
            '1980s': 'https://open.spotify.com/playlist/37i9dQZF1DXc3KygMa1OE7?si=d5ac64afe4b44c5e',
            '1990s': 'https://open.spotify.com/playlist/37i9dQZF1DWXqpDKK4ed9O?si=535db10c0a874802',
            '2000s': 'https://open.spotify.com/playlist/37i9dQZF1DXd0DyosUBZQ7?si=a175bb1526bf452f',
            '2010s': 'https://open.spotify.com/playlist/37i9dQZF1DWVTfbQdQ8l7H?si=ea5210729ef84f74',
            'All Time': 'https://open.spotify.com/playlist/37i9dQZF1DX7rOY2tZUw1k?si=266213fca22b41e5',}

st.title('Love in Pop Culture')
st.subheader('Modern Love: Writing and Deconstructing the Idea - CCC338 Creative Project')
st.markdown('[Akshat Punia](https://akshatpunia.com/)')

decade = st.slider('Select a decade', 1940, 2000, 1980, 10)

if st.button('Generate Playlist'):
    decade = str(decade) + 's'
    playlist_uri = decades[decade_str]
    