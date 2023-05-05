import streamlit as st
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

client_id = 'dc8611201d2a4d68ac59e3623d309096'
client_secret = '470122036a274706a4f705ab88867fed'
scope = 'user-library-read'
redirect_uri = 'https://modern-love-spotify.streamlit.app/'
auth_manager = SpotifyOAuth(client_id=client_id, client_secret=client_secret, scope=scope, redirect_uri=redirect_uri)
sp = spotipy.Spotify(auth_manager=auth_manager)

decades = {'1920s': 'https://open.spotify.com/playlist/7HWmbcjkVTfQdLKk2NWmtZ?si=6b870f33efe24872' ,
           '1930s': 'https://open.spotify.com/playlist/2webFRRyZuTUdw9KrMKT63?si=08ee3c375cba4319' ,
           '1940s': 'https://open.spotify.com/playlist/1KTSHAsbCgSnZLMdXp52Ln?si=93366e637d9349ca' ,
           '1950s': 'https://open.spotify.com/playlist/431BefAztO1PGCR4yd6PXL?si=231a737083dc4906'}

st.title('Love in Pop Culture')
st.subheader('Modern Love: Writing and Deconstructing the Idea - CCC338 Creative Project')
st.markdown('[Akshat Punia](https://akshatpunia.com/)')

decade = st.slider('Select a decade', 1920, 2010, 1980, 10)

if st.button('Generate Playlist'):
    decade_str = str(decade) + 's'
    if decade_str in decades:
        playlist_uri = decades[decade_str]
        playlist = sp.playlist_tracks(playlist_uri)
        tracks = playlist['items']
        tracks_uris = [track['track']['uri'] for track in tracks]
        sp.start_playback(uris=tracks_uris)
        st.write('Enjoy your custom playlist!')
    else:
        st.write('Sorry, no playlist found for this decade.')
