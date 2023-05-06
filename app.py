import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials

# Set up Spotipy with your app credentials
client_id = 'your_client_id_here'
client_secret = 'your_client_secret_here'
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

# Dictionary to map decade to playlist link
playlist_links = {
    '1920s': 'https://open.spotify.com/playlist/7HWmbcjkVTfQdLKk2NWmtZ?si=6b870f33efe24872',
    '1930s': 'https://open.spotify.com/playlist/2webFRRyZuTUdw9KrMKT63?si=08ee3c375cba4319',
    '1940s': 'https://open.spotify.com/playlist/1KTSHAsbCgSnZLMdXp52Ln?si=93366e637d9349ca',
    '1950s': 'https://open.spotify.com/playlist/431BefAztO1PGCR4yd6PXL?si=231a737083dc4906',
    '1960s': 'https://open.spotify.com/playlist/37i9dQZF1DWYUCqLrWKr4p?si=9231af5a094b4d58',
    '1970s': 'https://open.spotify.com/playlist/37i9dQZF1DWY373eEGlSj4?si=02b1f17f991141c3',
    '1980s': 'https://open.spotify.com/playlist/37i9dQZF1DXc3KygMa1OE7?si=d5ac64afe4b44c5e',
    '1990s': 'https://open.spotify.com/playlist/37i9dQZF1DWXqpDKK4ed9O?si=535db10c0a874802',
    '2000s': 'https://open.spotify.com/playlist/37i9dQZF1DXd0DyosUBZQ7?si=a175bb1526bf452f',
    '2010s': 'https://open.spotify.com/playlist/37i9dQZF1DWVTfbQdQ8l7H?si=ea5210729ef84f74',
    'All time': 'https://open.spotify.com/playlist/37i9dQZF1DX7rOY2tZUw1k?si=266213fca22b41e5'
}

# Initialize a list to store data for all playlists
all_tracks = []

# Loop through each decade and get its tracks
for decade, link in playlist_links.items():
    # Extract the playlist ID from the link
    playlist_id = link.split('/')[-1].split('?')[0]
    
    # Use Spotipy to get the playlist's tracks
    playlist = sp.playlist_tracks(playlist_id)
    tracks = playlist['items']
    
    # Loop through each track and extract its data
    for track in tracks:
        artist = track['track']['artists'][0]['name']
        name = track['track']['name']
        uri = track['track']['uri']
        all_tracks.append({'playlist_uri': link, 'artist': artist, 'name': name, 'decade': decade})

# Convert the list of tracks to a DataFrame and save as CSV
df = pd.DataFrame(all_tracks)
df.to_csv('playlist_data.csv', index=False)