from cgitb import reset
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Selected features that a song is given via Spotify API
SONG_FEATURES = ["acousticness", "danceability", "energy", "speechiness", "tempo", "valence"]

# All options for the action choice and its associated song features.
action_features = {
    'WORKINGOUT': {'acousticness': 0.125, 'danceability': 0.75, 'energy': 1, 'speechiness': 0.125, 'tempo': 135, 'valence': 0.5}, 
    'STUDYING': {'acousticness': 0.5, 'danceability': 0.125, 'energy': 0.125, 'speechiness': 0.33, 'tempo': 95, 'valence': 0.66}, 
    'DRIVING': {'acousticness': 0.125, 'danceability': 0.5, 'energy': 0.5, 'speechiness': 0.25, 'tempo': 125, 'valence': 0.5}, 
    'DANCING': {'acousticness': 0.25, 'danceability': 1, 'energy': 0.5, 'speechiness': 0.25, 'tempo': 115, 'valence': 0.75}, 
    'RELAXING': {'acousticness': 0.75, 'danceability': 0, 'energy': 0, 'speechiness': 0.5, 'tempo': 80, 'valence': 1},
}

# All options for the mood choice and its associated song features.
mood_features = {
    'ANGRY': {'acousticness': 0, 'danceability': 0.5, 'energy': 0.875, 'speechiness': 0.125, 'tempo': 150, 'valence': 0.125}, 
    'ANXIOUS': {'acousticness': 0.5, 'danceability': 0.33, 'energy': 0.125, 'speechiness': 0, 'tempo': 75, 'valence': 1}, 
    'ENERGIZED': {'acousticness': 0.125, 'danceability': 1, 'energy': 1, 'speechiness': 0.125, 'tempo': 145, 'valence': 0.5},       'JOYFULL': {'acousticness': 0.33, 'danceability': 0.25, 'energy': 0.33, 'speechiness': 0.5, 'tempo': 115, 'valence': 0.75}, 
    'SAD': {'acousticness': 0.5, 'danceability': 0.125, 'energy': 0.125, 'speechiness': 0.25, 'tempo': 80, 'valence': 0}, 
    'PEACEFUL': {'acousticness': 1, 'danceability': 0.125, 'energy': 0, 'speechiness': 0.66, 'tempo': 60, 'valence': 0.66}, 
    'TIRED': {'acousticness': 0.66, 'danceability': 0, 'energy': 0.25, 'speechiness': 0.5, 'tempo': 85, 'valence': 0.75}
}

genre_features = {

}


def select_audio_features(input):
    # authorization information
    CLIENT_ID = 'ecca6b6968774a20bc255c94ded4fbb4'
    CLIENT_SECRET = 'ccb019ba7bd9409f93f2527ea42f0e88'
    REDIRECT_URI = 'http://localhost'

    client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    songs = {}
    for song in input["favSongs"]:
        res = sp.search(q=song, limit=1, offset=0, type="track", market="US")
        song_id = res["tracks"]["items"][0]["id"]
        raw_features = sp.audio_features(song_id)
        songs[song] = cleanse_features(raw_features[0])

    features = {}
    action_feature = action_features[input["activities"][0]]
    mood_feature = mood_features[input["mood"]]
    for feature in SONG_FEATURES:
        features[feature] = 0
        for song in songs:
            temp_feature = join_instance_features(songs[song][feature], action_feature[feature], mood_feature[feature])
            features[feature] = features[feature] + temp_feature
        features[feature] = round(features[feature] / 3, 5)
    return features

def cleanse_features(features):
    clean_features = {}
    for feature in features:
        if feature in SONG_FEATURES:
            clean_features[feature] = features[feature]
    return clean_features

def join_instance_features(song_feature, action_feature, mood_feature):
    res = round((action_feature + mood_feature + song_feature + song_feature) / 4, 5)
    return res        

sample_input = {
    "INPUT":
        {
            "activities": ["RELAXING"],
            "favArtists": ["Avicii","Martin Garrix","Kanye West"],
            "favGenres": ["EDM","Rap","Pop"],
            "mood": "TIRED",
            "number": 50,
            "favSongs": ["Waiting for Love","High on Life","Homecoming"],
            "theme": ""
        },
    "OUTPUT":
        {
            "acousticness":1.08, 
            "danceability":0.0, 
            "energy":0.125, 
            "speechiness":0.75, 
            "tempo":122.5, 
            "valence":1.375
        }
    }
select_audio_features(sample_input["INPUT"])