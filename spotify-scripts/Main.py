import os
import pandas as pd
import numpy as np

from TrackGeneration import artistGeneratedTracks
from SongFeatures import getTracksAudioFeatures
from KMeans import kMeans, selectCluster
from SongAnalysis import moodFilterCluster

# read in csv file with artist name and uri pairs
script_dir = os.getcwd()
file = 'artist-uris.csv'
artistUriDf = pd.read_csv(os.path.normcase(os.path.join(script_dir, file)))

# this is where we will take input from the web app for liked artists to find similar ones
steveLacy = "spotify:artist:57vWImR43h4CaDao012Ofp"
dmx = "spotify:artist:1HwM5zlC5qNWhJtM00yXzG"
ledZeppelin = "spotify:artist:36QJpDe2go2KgaRleHCDTp"
duaLipa = "spotify:artist:6M2wZ9GZgrQXHCFfjv46we"
# steveSongs = artistRelatedTracks(steveLacy)
dmxSongs, dmxArtists = artistGeneratedTracks(dmx)
ledSongs, ledArtists = artistGeneratedTracks(ledZeppelin)
duaSongs, duaArtists = artistGeneratedTracks(duaLipa)

songList = np.unique([*dmxSongs, *ledSongs, *duaSongs])
artistList = np.unique([*dmxArtists, *ledArtists, *duaArtists])

# get the audio features of each song in the songlist
songDf = getTracksAudioFeatures(songList)

# use K-Means clustering to groups songs together based on the audio features
featureLabels = ["danceability", "energy", "loudness", "speechiness", "acousticness", "instrumentalness", "valence", "tempo"]
clusterDf = kMeans(songDf, featureLabels)

# determine what cluster to use based on the activity the user selected
activitySongs = selectCluster(clusterDf, 1)
# filter songs in the selected cluster based on the user selected mood
moodSongs = moodFilterCluster(activitySongs, 'HAPPY')