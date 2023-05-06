import pandas as pd
import streamlit as st
import random
import requests
import base64
from PIL import Image
st.set_page_config(layout='wide', page_title='CCC338 - Creative Project', page_icon=':heart:')

st.title("Modern Love: Writing and Deconstructing the Idea")
st.subheader("CCC338 - Creative Project - [Akshat Punia](https://akshatpunia.com/)")

st.header("Introduction")
st.write("I was always intrigued by how the idea of modern love has been displayed through pop art throughout the decades. By listening to these songs around the idea of love from various genres and time periods, we can gain a better understanding of this idea of modern love has evolved and continues to evolve.")

image = 'elvis.png'
st.image(image, caption='Elvis Presley Performing')

st.header("The Evolution of Love in Pop Art")
st.write("From the crooners of the 1930s to the rock ballads of the 1980s and beyond, love songs have always been a staple of pop culture. The lyrics and melodies have evolved with each decade, giving us a glimpse into the larger trends of the time.")    
st.write("For example, in the 1930s and 1940s, love songs were often about longing and unrequited love. With the rise of the rock and roll in the 1950s and 1960s, love songs became more upbeat and focused on the excitement and passion of falling in love. In the 1970s and 1980s, love songs took a turn towards heartbreak and loss, with artists exploring the pain of failed relationships and unrequited love.")
st.write("Despite these changes, the underlying theme of love has remained a constant throughout pop art. By analyzing the love songs of each decade, we can gain a better understanding of how love has been perceived and experienced by society.")

st.write("To further explore the idea of modern love, I (unsucessfully to my original idea) created this webapp. By selecting two decades, the generator will create a playlist of 20 random songs (10 from each decade). This playlist can be used to explore the themes and trends of love throughout the decades.")

playlist_data = pd.read_csv('playlist_data.csv')
client_id = 'dc8611201d2a4d68ac59e3623d309096'
client_secret = '470122036a274706a4f705ab88867fed'
credentials = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
headers = {
    'Authorization': f"Basic {credentials}"
}
token_url = 'https://accounts.spotify.com/api/token'
response = requests.post(token_url, 
                         data={'grant_type': 'client_credentials'},
                         headers=headers)
access_token = response.json()['access_token']
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
    def get_image_url(row):
        search_url = 'https://api.spotify.com/v1/search'
        query = f"{row['name']} {row['artist']}"
        response = requests.get(search_url, 
                                params={'q': query, 'type': 'track'}, 
                                headers={'Authorization': f'Bearer {access_token}'})
        track_id = response.json()['tracks']['items'][0]['id']
        track_url = f'https://api.spotify.com/v1/tracks/{track_id}'
        response = requests.get(track_url, headers={'Authorization': f'Bearer {access_token}'})
        image_url = response.json()['album']['images'][0]['url']
        return image_url
    st.markdown(f"## Your {decade1} + {decade2} Mixtape")
    st.subheader('(linked to playlists, instead of individual songs, due to Spotify API limitations')
    playlist['image_url'] = playlist.apply(get_image_url, axis=1)
    playlist['spotify_link'] = playlist.apply(lambda x: f"[Spotify]({x['playlist_uri']})", axis=1)
    for i, row in playlist.iterrows():
        st.write(f"{i+1}.")
        col1, col2 = st.beta_columns(2)
        with col1:
            st.image(row['image_url'], width=200)
        with col2:
            st.markdown(f"## **{row['name']}** by {row['artist']} ({row['decade']})\n{row['spotify_link']}")

