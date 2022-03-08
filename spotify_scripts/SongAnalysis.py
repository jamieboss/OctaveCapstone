from SpotifyOAuth import sp

# vectors for each mood representing intensity, timbre, pitch, and rhythm
HAPPY = [0.5, 0.5, 0.9, 0.9]
EXUBERANT = [0.7, 0.5, 0.7, 0.7]
ENERGETIC = [0.9, 0.5, 0.5, 0.7]
FRANTIC = [0.7, 0.9, 0.3, 0.9]
SAD = [0.5, 0.1, 0.1, 0.3]
DEPRESSION = [0.3, 0.3, 0.3, 0.3]
CALM = [0.1, 0.1, 0.5, 0.1]
CONTENTMENT = [0.3, 0.3, 0.7, 0.3]

# function that will filter a given cluster based on mood using songs audio analysis
def moodFilterCluster(cluster, mood):
    print(len(cluster))
    for song in cluster:
        anaylsis = sp.audio_analysis(song)
    