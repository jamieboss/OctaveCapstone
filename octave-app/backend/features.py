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
        'ENERGIZED': {'acousticness': 0.125, 'danceability': 1, 'energy': 1, 'speechiness': 0.125, 'tempo': 145, 'valence': 0.5}, 
        'JOYFULL': {'acousticness': 0.33, 'danceability': 0.25, 'energy': 0.33, 'speechiness': 0.5, 'tempo': 115, 'valence': 0.75}, 
        'SAD': {'acousticness': 0.5, 'danceability': 0.125, 'energy': 0.125, 'speechiness': 0.25, 'tempo': 80, 'valence': 0}, 
        'PEACEFUL': {'acousticness': 1, 'danceability': 0.125, 'energy': 0, 'speechiness': 0.66, 'tempo': 60, 'valence': 0.66}, 
        'TIRED': {'acousticness': 0.66, 'danceability': 0, 'energy': 0.25, 'speechiness': 0.5, 'tempo': 85, 'valence': 0.75}
        }


def audio_features(action, mood):
    """
    Returns a dict of features with calculated values for each song feature based on provided action and mood.

    :param action: str action type selection (i.e. WORKINGOUT, STUDYING)
    :param mood: str mood type selection (i.e. ANGRY, ANXIOUS)
    :return: a dict of features
    """
    features = {}
    for feature in SONG_FEATURES:
        features[feature] = set_feature(action, mood, feature)
    return features

def set_feature(action, mood, feature):
    """
    Helper function of audio_features to calculate the song features for a choice of action and mood. 
    Current algorithm is to return the average of the two values.

    :param action: str action type selection (i.e. WORKINGOUT, STUDYING)
    :param mood: str mood type selection (i.e. ANGRY, ANXIOUS)
    :param feature: str feature from SONG_FEATURES (i.e. acousticness, danceability)
    :return: a float value of the assigned feature
    """
    res = round(action_features[action][feature] + mood_features[mood][feature] / 2, 5)
    return res        