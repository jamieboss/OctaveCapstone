from email.policy import default
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# authorization information
CLIENT_ID = 'f54a10c8ab084526a1df90b9c7f4f19f'
CLIENT_SECRET = '2178e29186714432b61020743e950821'
REDIRECT_URI = 'http://localhost'

scope = 'playlist-modify-public'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=scope))