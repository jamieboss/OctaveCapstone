import os
import pandas as pd
import numpy as np

from TrackGeneration import artistGeneratedTracks, genreGeneratedTracks
from SongFeatures import getTracksAudioFeatures
from KMeans import kMeans, selectCluster
from SongAnalysis import moodFilterCluster

# read in csv file with artist name and uri pairs
script_dir = os.getcwd()
file = 'artist-uris.csv'
artistUriDf = pd.read_csv(os.path.normcase(os.path.join(script_dir, file)), names=['name', 'uri'])

# this is where we will take input from the web app for liked artists to find similar ones
artist1 = "spotify:artist:57vWImR43h4CaDao012Ofp"
artist2 = "spotify:artist:1HwM5zlC5qNWhJtM00yXzG"
artist3 = "spotify:artist:36QJpDe2go2KgaRleHCDTp"
artist1Songs, artist1Artists = artistGeneratedTracks(artist1)
artist2Songs, artist2Artists = artistGeneratedTracks(artist2)
artist3Songs, artist3Artists = artistGeneratedTracks(artist3)

genre1Songs = genreGeneratedTracks("rock")
genre2Songs = genreGeneratedTracks("rap")
genre3Songs = genreGeneratedTracks("pop")

songList = np.unique([*artist1Songs, *artist2Songs, *artist3Songs, *genre1Songs, *genre2Songs, *genre3Songs])
# artistList = np.unique([*dmxArtists, *ledArtists, *duaArtists])

# get the audio features of each song in the songlist
songDf = getTracksAudioFeatures(songList)

# use K-Means clustering to groups songs together based on the audio features
featureLabels = ["danceability", "energy", "loudness", "speechiness", "acousticness", "instrumentalness", "valence", "tempo"]
clusterDf, numClusters = kMeans(songDf, featureLabels)

# # determine what cluster to use based on the activity the user selected
# activitySongs = selectCluster(clusterDf, numClusters, "Studying")
# # filter songs in the selected cluster based on the user selected mood
# moodSongs = moodFilterCluster(activitySongs, 'HAPPY')