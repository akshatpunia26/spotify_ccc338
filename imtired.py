import spotipy
from spotipy.oauth2 import SpotifyOAuth

client_id = "dc8611201d2a4d68ac59e3623d309096"
client_secret = "470122036a274706a4f705ab88867fed"
redirect_uri = "http://localhost:8888/callback/"

auth_manager = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope="playlist-modify-public")

auth_url = auth_manager.get_authorize_url()
print(auth_url)
