from email.policy import default
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# authorization information
CLIENT_ID = 'ecca6b6968774a20bc255c94ded4fbb4'
CLIENT_SECRET = 'ccb019ba7bd9409f93f2527ea42f0e88'
REDIRECT_URI = 'http://localhost'

scope = 'user-library-read'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=scope))