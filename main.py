import pandas as pd
import streamlit as st

playlist_data = pd.read_csv('playlist_data.csv')

st.title('Decades Playlist Generator')
st.markdown("""Select two decades from 1920 to 2010, and we'll generate a playlist of all songs from each decade!""")

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

if st.button('Generate Playlist'):
    playlist1 = playlist_data[playlist_data['decade'] == decade1]
    playlist2 = playlist_data[playlist_data['decade'] == decade2]
    st.markdown(f"## Your {decade1} + {decade2} Playlist")
    st.write(f"### {decade1}")
    for index, row in playlist1.iterrows():
        st.write(f"[{row['name']} - {row['artist']}]({row['playlist_uri']})")
    st.write(f"### {decade2}")
    for index, row in playlist2.iterrows():
        st.write(f"[{row['name']} - {row['artist']}]({row['playlist_uri']})")
