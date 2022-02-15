import random
import time
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# authorization information
CLIENT_ID = 'ecca6b6968774a20bc255c94ded4fbb4'
CLIENT_SECRET = 'ccb019ba7bd9409f93f2527ea42f0e88'
REDIRECT_URI = 'http://localhost'

client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

NUM_INIT_ARTISTS = 5
NUM_ALBUMS_ARTIST = 2
NUM_TRACKS_ALBUM = 4


# function for getting related artists
def getRelatedArtists(artistId, depth=1, numArtists=3):
    artists = sp.artist_related_artists(artistId)['artists']
    if len(artists) > numArtists:
        artists = random.sample(artists, numArtists)
    # recursively call the getRelatedArtists function to get artists related to the related artist
    if depth > 1:
        artistLayer = [artist for artist in artists]
        for artist in artists:
            artists = getRelatedArtists(artist['id'], depth-1, 2)
            artistLayer = artistLayer + artists
        artists = artistLayer
    return artists

# function to get random tracks per album
def getRandomTracks(tracks):
    randTracks = []
    if len(tracks) > NUM_TRACKS_ALBUM:
        randTracks = random.sample([track['id'] for track in tracks], NUM_TRACKS_ALBUM)
    else:
        randTracks = [track['id'] for track in tracks]
    return randTracks

# this is where we will take input from the web app for liked artists to find similar ones
steveLacy = "spotify:artist:57vWImR43h4CaDao012Ofp"
# random depth search for related artists to possibly find unlistened to music
mostSimilarArtists = getRelatedArtists(steveLacy, 0, NUM_INIT_ARTISTS)
# create a depth map for how deep we will search for each artist
artistDepths = [random.randint(0,2) for i in range(len(mostSimilarArtists))]
# list of ids for all of the related artists
relatedArtistIds = [artist['id'] for artist in mostSimilarArtists]

# loop over most similar artists and continue adding related artists depending on the depth map
for i, artist in enumerate(mostSimilarArtists):
    if artistDepths[i] >= 1:
        artists = getRelatedArtists(artist['id'], artistDepths[i])
        for a in artists:
            if a['id'] not in relatedArtistIds:
                relatedArtistIds.append(a['id'])
    
relatedArtistIds = random.sample(relatedArtistIds, 5)

preclassifiedTracks = []
for artistId in relatedArtistIds:
    # get all of the artists albums
    artistAlbums = sp.artist_albums(artistId)['items']
    # store the ids of the albumns to do create an efficient request
    albumIds = []
    if len(artistAlbums) > NUM_ALBUMS_ARTIST:
        albumIds = random.sample([album['id'] for album in artistAlbums], NUM_ALBUMS_ARTIST)
    else:
        albumIds = [album['id'] for album in artistAlbums]
    # gets the tracks from the returned albums
    albums = sp.albums(albumIds)['albums']
    # list of tracks to be used in the mood classification

    if len(albums) >= NUM_ALBUMS_ARTIST:
        for i in range(NUM_ALBUMS_ARTIST):
            tracks = albums[i]['tracks']['items']
            preclassifiedTracks = preclassifiedTracks + getRandomTracks(tracks)
    else:
        print("Only one album :(")
        tracks = albums['tracks']['items']
        preclassifiedTracks = preclassifiedTracks + getRandomTracks(tracks)

# makes sure all tracks in the list are unique
preclassifiedTracks = np.unique(np.array(preclassifiedTracks))
print(preclassifiedTracks)