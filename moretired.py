import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Set up authentication manager
CLIENT_ID = 'dc8611201d2a4d68ac59e3623d309096'
CLIENT_SECRET = '470122036a274706a4f705ab88867fed'
REDIRECT_URI = 'http://localhost:8888/callback/'
SCOPE = 'user-library-read'
CACHE_PATH = '.spotipyoauthcache'

auth_manager = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE,
    cache_path=CACHE_PATH,
)

# Get access token
auth_code = 'AQA9_RaCEb8UJq5hR-knBtBhlF45EUISfn_NlTh8JYH0J2pm_eWK2YrW2wC3VbYgNPGS-VRXyglsEwH7PAQSVJcOlEMgADPvdvNgxxm572Zssav_a8Ykas24rzHSd03YXrJdXkLPAEkThlX4WwrsyI1I2EFSwk1JuI-zVX4Yk_QbnKGsQmKCu0IpwZ6Iln7CwCT7YbfP3drgB0A'
access_token = auth_manager.get_access_token(auth_code, as_dict=False)

# Use access token to get current user
spotify = spotipy.Spotify(auth_manager=auth_manager)
user_dict = spotify.current_user()

# Print user details
print(user_dict)
