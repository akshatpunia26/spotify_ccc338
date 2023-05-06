import pandas as pd
import streamlit as st
import random
import requests
import base64

# Load playlist data
playlist_data = pd.read_csv('playlist_data.csv')

# Set page title
st.set_page_config(page_title='Modern Love: In Writing', page_icon=':heart:')

# Spotify API credentials
client_id = 'dc8611201d2a4d68ac59e3623d309096'
client_secret = '470122036a274706a4f705ab88867fed'

# Base64 encode credentials
credentials = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

# Set headers
headers = {
    'Authorization': f"Basic {credentials}"
}

# Get access token
token_url = 'https://accounts.spotify.com/api/token'
response = requests.post(token_url, 
                         data={'grant_type': 'client_credentials'},
                         headers=headers)
access_token = response.json()['access_token']

# Decades selector
decades_dict = {'1920s': 1920,
                '1930s': 1930,
                '1940s': 1940,
                '1950s': 1950,
                '1960s': 1960,
                '1970s': 1970,
                '1980s': 1980,
                '1990s': 1990,
                '2000s': 2000,
                '2010s': 2010}
decades = list(decades_dict.keys())

decade1 = st.selectbox('Select the first decade:', decades)
decade2 = st.selectbox('Select the second decade:', decades)

start_year1 = decades_dict[decade1]
end_year1 = start_year1 + 10
start_year2 = decades_dict[decade2]
end_year2 = start_year2 + 10

if st.button('Generate Playlist'):
    playlist1 = playlist_data[(playlist_data['decade'] == decade1)]
    playlist1 = playlist1.sample(n=min(10, len(playlist1)))
    playlist2 = playlist_data[(playlist_data['decade'] == decade2)]
    playlist2 = playlist2.sample(n=min(10, len(playlist2)))
    playlist = pd.concat([playlist1, playlist2]).reset_index(drop=True)
    st.markdown(f"## Your {decade1} + {decade2} Playlist")
    for index, row in playlist.iterrows():
        # Get album art image from Spotify API
        search_url = 'https://api.spotify.com/v1/search'
        query = f"{row['name']} {row['artist']}"
        response = requests.get(search_url, 
                                params={'q': query, 'type': 'track'}, 
                                headers={'Authorization': f'Bearer {access_token}'})
        track_id = response.json()['tracks']['items'][0]['id']
        track_url = f'https://api.spotify.com/v1/tracks/{track_id}'
        response = requests.get(track_url, headers={'Authorization': f'Bearer {access_token}'})
        image_url = response.json()['album']['images'][0]['url']
        
        # Display song info and album art
        st.write(f"**{row['name']}** by {row['artist']} ({row['decade']}s)")
        st.image(image_url, width=200)
        st.write(f"Listen on [Spotify]({row['playlist_uri']})\n")
