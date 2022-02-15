import spotipy
import numpy as np
import pandas as pd


from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = 'f54a10c8ab084526a1df90b9c7f4f19f'
CLIENT_SECRET = '2178e29186714432b61020743e950821'
REDIRECT_URI = 'http://localhost/'
scope = 'user-library-read'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=scope))


#read from database
df = pd.read_csv("artist-uris.csv.csv")
df.head
IDs = df.iloc[:,1]

#temporary Artist id assignment from database
ArtistID = IDs[1173]
artist = sp.artist(ArtistID)
artistName = artist['name']
print(artistName)


#get all of artists albums
albums = sp.artist_albums(artist['id'])['items']
album_ids = []
#get albums from artist
for album in albums:
    album_ids.append(album['id'])
#get tracks from albums
track_list = sp.albums(album_ids)['albums']
#retrieve name and featuures of songs
for i in range(5):
    tracks = tracks = track_list[i]['tracks']['items']
    for j in range(3):
        name = tracks[j]['name']
        uri = tracks[j]['uri']
        trackFeats = sp.audio_features(uri)
        print(name)
        print(trackFeats)
        print()
