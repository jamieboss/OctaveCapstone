import spotipy
from spotipy.oauth2 import SpotifyOAuth

# authorization information
CLIENT_ID = 'f54a10c8ab084526a1df90b9c7f4f19f'
CLIENT_SECRET = '2178e29186714432b61020743e950821'
REDIRECT_URI = 'http://localhost/'

scope = 'user-library-read'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=scope))

# this is where we will take input from the web app for liked artists to find similar ones
steve_lacy = "spotify:artist:57vWImR43h4CaDao012Ofp"
artists = sp.artist_related_artists(steve_lacy)['artists']

# loops over all related artists
for artist in artists:
    print(artist['name'])
    # get all of the artists albums
    albums = sp.artist_albums(artist['id'])['items']
    # store the ids of the albumns to do create an efficient request
    album_ids = []
    for album in albums:
        album_ids.append(album['id'])
    # gets the tracks from the returned albums
    track_list = sp.albums(album_ids)['albums']
    for i in range(2):
        tracks = track_list[i]['tracks']['items']
        for j in range(1):
            print(tracks[j]['name'])
    print()
