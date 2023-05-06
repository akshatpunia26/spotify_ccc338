import pandas as pd
import streamlit as st
import random

# Load playlist data
playlist_data = pd.read_csv('playlist_data.csv')

# Set page title
st.set_page_config(page_title='Modern Love: In Writing', page_icon=':heart:')

# Page heading and synopsis
st.title('Modern Love: In Writing')
st.markdown('''
The idea of modern love has evolved over the years, and popular music has played a significant role in shaping our understanding of what love means in different eras. From the romantic ballads of the 1950s to the more complex and nuanced portrayals of love in recent times, pop songs have reflected changing social norms, cultural attitudes, and personal experiences.

With this tool, you can explore the evolution of modern love by generating a playlist of the top 10 pop songs from two different decades. Simply select your preferred decades from the dropdown menus and click the "Generate Playlist" button to get started!
''')

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
        st.write(f"[{row['name']} by {row['artist']}](row['playlist_uri'])")