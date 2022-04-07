from cgitb import reset
import spotipy

# Selected features that a song is given via Spotify API
SONG_FEATURES = ["acousticness", "danceability", "energy", "speechiness", "tempo", "valence"]

# All options for the action choice and its associated song features.
action_features = {
    'WORKING OUT': {'acousticness': [0, 0.3], 'danceability': [0.7, 1], 'energy': [0.8, 1], 'speechiness': [0, 1], 'tempo': [120, 200], 'valence': [0, 1]}, 
    'STUDYING': {'acousticness': [0.5, 1], 'danceability': [0, 0.3], 'energy': [0, 0.3], 'speechiness': [0, 0.2], 'tempo': [80, 160], 'valence': [0, 1]}, 
    'DRIVING': {'acousticness': [0.3, 0.9], 'danceability': [0, 0.5], 'energy': [0, 0.5], 'speechiness': [0.5, 1], 'tempo': [80, 200], 'valence': [0, 1]}, 
    'DANCING': {'acousticness': [0, 1], 'danceability': [0.8, 1], 'energy': [0.8, 1], 'speechiness': [0.2, 0.8], 'tempo': [120, 200], 'valence': [0, 1]}, 
    'RELAXING': {'acousticness': [0, 1], 'danceability': [0, 0.3], 'energy': [0, 0.3], 'speechiness': [0, 1], 'tempo': [60, 120], 'valence': [0, 1]}, 
}

# All options for the mood choice and its associated song features.
mood_features = {
    'ANGRY': {'acousticness': [0, 0.3], 'danceability': [0.7, 1], 'energy': [0.8, 1], 'speechiness': [0, 1], 'tempo': [120, 200], 'valence': [0, 1]}, 
    'ANXIOUS': {'acousticness': [0.3, 0.9], 'danceability': [0, 0.5], 'energy': [0, 0.5], 'speechiness': [0.5, 1], 'tempo': [80, 200], 'valence': [0, 1]}, 
    'ENERGIZED': {'acousticness': [0, 1], 'danceability': [0.8, 1], 'energy': [0.8, 1], 'speechiness': [0.2, 0.8], 'tempo': [120, 200], 'valence': [0, 1]}, 
    'JOYFUL': {'acousticness': [0, 1], 'danceability': [0.8, 1], 'energy': [0.8, 1], 'speechiness': [0.2, 0.8], 'tempo': [120, 200], 'valence': [0, 1]}, 
    'SAD': {'acousticness': [0.5, 1], 'danceability': [0, 0.3], 'energy': [0, 0.3], 'speechiness': [0, 0.2], 'tempo': [80, 160], 'valence': [0, 1]}, 
    'PEACEFUL': {'acousticness': [0, 1], 'danceability': [0, 0.3], 'energy': [0, 0.3], 'speechiness': [0, 1], 'tempo': [60, 120], 'valence': [0, 1]}, 
    'TIRED': {'acousticness': [0.5, 1], 'danceability': [0, 0.3], 'energy': [0, 0.3], 'speechiness': [0, 0.2], 'tempo': [80, 160], 'valence': [0, 1]}, 
}

genre_features = {

}


# def select_audio_features(input):
#     # authorization information
#     CLIENT_ID = 'ecca6b6968774a20bc255c94ded4fbb4'
#     CLIENT_SECRET = 'ccb019ba7bd9409f93f2527ea42f0e88'
#     REDIRECT_URI = 'http://localhost'

#     client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
#     sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#     songs = {}
#     for song in input["favSongs"]:
#         res = sp.search(q=song, limit=1, offset=0, type="track", market="US")
#         song_id = res["tracks"]["items"][0]["id"]
#         raw_features = sp.audio_features(song_id)
#         songs[song] = cleanse_features(raw_features[0])

#     features = {}
#     action_feature = action_features[input["activities"][0]]
#     mood_feature = mood_features[input["mood"]]
#     for feature in SONG_FEATURES:
#         features[feature] = 0
#         for song in songs:
#             temp_feature = join_instance_features(songs[song][feature], action_feature[feature], mood_feature[feature])
#             features[feature] = features[feature] + temp_feature
#         features[feature] = round(features[feature] / 3, 5)
#     return features

# def cleanse_features(features):
#     clean_features = {}
#     for feature in features:
#         if feature in SONG_FEATURES:
#             clean_features[feature] = features[feature]
#     return clean_features

# def join_instance_features(song_feature, action_feature, mood_feature):
#     res = round((action_feature + mood_feature + song_feature + song_feature) / 4, 5)
#     return res        

# sample_input = {
#     "INPUT":
#         {
#             "activities": ["RELAXING"],
#             "favArtists": ["Avicii","Martin Garrix","Kanye West"],
#             "favGenres": ["EDM","Rap","Pop"],
#             "mood": "TIRED",
#             "number": 50,
#             "favSongs": ["Waiting for Love","High on Life","Homecoming"],
#             "theme": ""
#         },
#     "OUTPUT":
#         {
#             "acousticness":1.08, 
#             "danceability":0.0, 
#             "energy":0.125, 
#             "speechiness":0.75, 
#             "tempo":122.5, 
#             "valence":1.375
#         }
#     }
# select_audio_features(sample_input["INPUT"])