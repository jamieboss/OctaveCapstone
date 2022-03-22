import numpy as np

from SpotifyOAuth import sp

# function that will filter a given cluster based on mood using songs audio analysis
def moodFilterCluster(cluster, mood):
    for song in cluster:
        pitch, timbre = pitchAndTimbre(song)

        # print('\n', pitch)
        # print(timbre, '\n')

# gets a songs average pitch and timbre vectors
def pitchAndTimbre(song):
    pitchSum = np.zeros(12)
    timbreSum = np.zeros(12)

    segments = sp.audio_analysis(song)['segments']
    for segment in segments:
        pitchSum = np.add(pitchSum, segment['pitches'])
        timbreSum = np.add(timbreSum, segment['timbre'])

    averagePitch = pitchSum / len(segments)
    averageTimbre = timbreSum / len(segments)

    # normalize the pitch vector
    normalPitch = [(averagePitch[i] - np.min(averagePitch))/(np.max(averagePitch) - np.min(averagePitch)) for i in range(12)]
    return normalPitch, averageTimbre