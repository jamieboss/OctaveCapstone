import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = 'f54a10c8ab084526a1df90b9c7f4f19f'
CLIENT_SECRET = '2178e29186714432b61020743e950821'
REDIRECT_URI = 'http://localhost/'

scope = 'user-library-read'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=scope))

steve_lacy = "spotify:artist:57vWImR43h4CaDao012Ofp"
artist = sp.artist(steve_lacy)

print(artist)