import os
import numpy as np
import pandas as pd
import csv
from SpotifyOAuth import sp

#read from database
script_dir = os.getcwd()
file = 'artist-uris.csv'
df = pd.read_csv(os.path.normcase(os.path.join(script_dir, file)))
df.head
#gets list of all spotify artist ids,
#IDs = df.iloc[:,1]

def getTrackIdsForAllArtists():
    #tempooorary list oof spotify artisst ids
    # IDs = ["spotify:artist:3ApUX1o6oSz321MMECyIYd?si=9JtOb6KKSNm1boeBYvyTFg"]

    # Getting list of all artist IDs in artist-uris.csv. Taking 1/100 artists as a subset to save time.
    artistIds = []
    # count = 0
    # with open('artist-uris.csv', 'r', encoding='utf-8') as csvfile:
    #     artist_reader = csv.reader(csvfile)
    #     for row in artist_reader:
    #         if count % 100 == 0:
    #             artistIds.append(row[1])
    #         count+=1

    all_songs = []
    for ArtistID in artistIds:
        artist = sp.artist(ArtistID)
        artistName = artist['name']
        #get all of artists albums
        albums = sp.artist_albums(artist['id'])['items']
        album_ids = []
        #get albums from artist
        for album in albums:
            album_ids.append(album['id'])
        #get tracks from albums
        if (len(album_ids) > 0):
            track_list = sp.albums(album_ids)['albums']
            #retrieve name and features of songs
            for i in range(len(track_list)):
                tracks =  track_list[i]['tracks']['items']
                for j in range(len(tracks)):
                    all_songs.append(tracks[j]['id'])
                    # name = tracks[j]['name']
                    # uri = tracks[j]['uri']
                    # trackFeats = sp.audio_features(uri)
    return all_songs     

# gets to audio features for each track in the id list and stores it in a dataframe
def getTracksAudioFeatures(trackIds):
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

# Getting ~10000 songs and all the features for them from a huge spotify playlist. This is good enough for our purposes to populate elastic search.
def get_tracks_for_es():
    songIds = []
    for i in range(100): # playlist_tracks has limit of 100, has 10k songs, 100 * 100 = 10k
        tracks = sp.playlist_tracks(playlist_id='6yPiKpy7evrwvZodByKvM9', offset=i*100)
        for j in range(len(tracks['items'])):
            id = tracks['items'][j]['track']['uri'][-22:] # ID is last 22 characters of string. Sometimes this returns a artist name randomly with +s, so calling isalnum() to ensure id
            if len(id) != 0 and id.isalnum():
                songIds.append(id)
    features = getTracksAudioFeatures(songIds)
    return features
