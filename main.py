import pandas as pd
import streamlit as st

playlist_data = pd.read_csv('playlist_data.csv')

st.title('Decades Playlist Generator')
st.markdown("""Select two decades from 1920 to 2010, and we'll generate a playlist of the top 20 songs from each decade!""")

decades_dict = {1920: '1920s',
                1930: '1930s',
                1940: '1940s',
                1950: '1950s',
                1960: '1960s',
                1970: '1970s',
                1980: '1980s',
                1990: '1990s',
                2000: '2000s',
                2010: '2010s'}
decades = list(decades_dict.values())

decade1 = st.selectbox('Select the first decade:', decades)
decade2 = st.selectbox('Select the second decade:', decades)

start_year1 = int(decade1[:4])
end_year1 = start_year1 + 9
start_year2 = int(decade2[:4])
end_year2 = start_year2 + 9

if st.button('Generate Playlist'):
    playlist1 = playlist_data[(playlist_data['decade'] == start_year1) & (playlist_data['playlist_uri'].str.contains(str(start_year1))) & (playlist_data['playlist_uri'].str.contains(str(end_year1)))].head(20)
    playlist2 = playlist_data[(playlist_data['decade'] == start_year2) & (playlist_data['playlist_uri'].str.contains(str(start_year2))) & (playlist_data['playlist_uri'].str.contains(str(end_year2)))].head(20)
    playlist = pd.concat([playlist1, playlist2]).reset_index(drop=True)
    st.markdown(f"## Your {decade1} + {decade2} Playlist")
    st.write(playlist[['artist', 'name']])