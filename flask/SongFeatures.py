import os
import numpy as np
import pandas as pd
from SpotifyOAuth import sp

#read from database
script_dir = os.getcwd()
file = 'artist-uris.csv'
df = pd.read_csv(os.path.normcase(os.path.join(script_dir, file)))
df.head
#gets list of all spotify artist ids,
#IDs = df.iloc[:,1]

def artistSongAttributes():
    #tempooorary list oof spotify artisst ids
    IDs = ["spotify:artist:3ApUX1o6oSz321MMECyIYd?si=9JtOb6KKSNm1boeBYvyTFg"]

    for ArtistID in IDs:
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
        #retrieve name and features of songs
        for i in range(len(track_list)):
            tracks =  track_list[i]['tracks']['items']
            for j in range(len(tracks)):
                
                name = tracks[j]['name']
                uri = tracks[j]['uri']
                trackFeats = sp.audio_features(uri)
                print(name)
                print(trackFeats)
                print()

# gets to audio features for each track in the id list and stores it in a dataframe
def getTracksAudioFeatures(trackIds):
    print(len(trackIds))
    trackDf = pd.DataFrame(columns=['name', 'artist', 'uri', "danceability", "energy", "loudness", "speechiness", "acousticness", "instrumentalness", "valence", "tempo"])
    # get track info and audio features for each track in the list
    oldIndex = 0
    for i in range(50,len(trackIds), 50):
        addTracksToDataframe(trackDf, trackIds, oldIndex, i)
        oldIndex = i
    
    # get the remainder of the songs in the list
    addTracksToDataframe(trackDf, trackIds, oldIndex, len(trackIds))

    return trackDf

# gets the row to be added to the dataframe
def addTracksToDataframe(trackDf, trackIds, startIndex, stopIndex):
    trackInfo = sp.tracks(trackIds[startIndex:stopIndex])['tracks']
    audioFeatures = sp.audio_features(trackIds[startIndex:stopIndex])

    for track, features in zip(trackInfo, audioFeatures):
        feature_subset = [features[feature] for feature in features if feature in ["acousticness", "danceability", "energy", "instrumentalness", "loudness", "speechiness", "valence", "tempo"]]
        row = [track['name'], track['artists'][0]['name'], track['uri'], *feature_subset]
        trackDf.loc[len(trackDf)] = row