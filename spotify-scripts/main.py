from random import random

# Selected features that a song is given via Spotify API
SONG_FEATURES = ["acousticness", "danceability", "energy", "instrumentalness", "loudness", "speechiness", "tempo", "valence"]

# All options for the action choice and its associated song features.
action_features = {
        'WORKINGOUT': {'acousticness': 0.125, 'danceability': 0.75, 'energy': 1, 'instrumentalness': 0.125, 'loudness': -50, 'speechiness': 0.125, 'tempo': 135, 'valence': 0.5}, 
        'STUDYING': {'acousticness': 0.5, 'danceability': 0.125, 'energy': 0.125, 'instrumentalness': 0.5,  'loudness': -15, 'speechiness': 0.33, 'tempo': 95, 'valence': 0.66}, 
        'DRIVING': {'acousticness': 0.125, 'danceability': 0.5, 'energy': 0.5, 'instrumentalness': 0.33, 'loudness': -40, 'speechiness': 0.25, 'tempo': 125, 'valence': 0.5}, 
        'DANCING': {'acousticness': 0.25, 'danceability': 1, 'energy': 0.5, 'instrumentalness': 0.25, 'loudness': -30, 'speechiness': 0.25, 'tempo': 115, 'valence': 0.75}, 
        'RELAXING': {'acousticness': 0.75, 'danceability': 0, 'energy': 0, 'instrumentalness': 0.66, 'loudness': -5, 'speechiness': 0.5, 'tempo': 80, 'valence': 1},
        'CLEANING': {'acousticness': 0.5, 'danceability': 0.25, 'energy': 0.25, 'instrumentalness': 0.33, 'loudness': -10, 'speechiness': 0.33, 'tempo': 100, 'valence': 0.75}
        }

# All options for the mood choice and its associated song features.
mood_features = {
        'ANGRY': {'acousticness': 0, 'danceability': 0.5, 'energy': 0.875, 'instrumentalness': 0.125, 'loudness': -60, 'speechiness': 0.125, 'tempo': 150, 'valence': 0.125}, 
        'ANXIOUS': {'acousticness': 0.5, 'danceability': 0.33, 'energy': 0.125, 'instrumentalness': 0.5, 'loudness': -10, 'speechiness': 0, 'tempo': 75, 'valence': 1}, 
        'ENERGIZED': {'acousticness': 0.125, 'danceability': 1, 'energy': 1, 'instrumentalness': 0.125, 'loudness': -35, 'speechiness': 0.125, 'tempo': 145, 'valence': 0.5}, 
        'AMUSED': {'acousticness': 0.33, 'danceability': 0.25, 'energy': 0.33, 'instrumentalness': 0.5, 'loudness': -25, 'speechiness': 0.5, 'tempo': 115, 'valence': 0.75}, 
        'MELANCHOLY': {'acousticness': 0.5, 'danceability': 0.125, 'energy': 0.125, 'instrumentalness': 0.75, 'loudness': -5, 'speechiness': 0.25, 'tempo': 80, 'valence': 0}, 
        'EMPOWERED': {'acousticness': 0.25, 'danceability': 0.875, 'energy': 0.75, 'instrumentalness': 0.25, 'loudness': -40, 'speechiness': 0.33, 'tempo': 95, 'valence': 0.875}, 
        'DEFIANT': {'acousticness': 0.125, 'danceability': 0.66, 'energy': 0.75, 'instrumentalness': 0.125, 'loudness': -35, 'speechiness': 0.33, 'tempo': 120, 'valence': 0.33}, 
        'FEARFUL': {'acousticness': 0.25, 'danceability': 0.5, 'energy': 0.66, 'instrumentalness': 0.33, 'loudness': -20, 'speechiness': 0.5, 'tempo': 100, 'valence': 0.875}, 
        'CHEERFUL': {'acousticness': 0.5, 'danceability': 0.75, 'energy': 0.5, 'instrumentalness': 0.25, 'loudness': -30, 'speechiness': 0.25, 'tempo': 110, 'valence': 1}, 
        'CHARMING': {'acousticness': 0.5, 'danceability': 0.75, 'energy': 0.5, 'instrumentalness': 0.25, 'loudness': -30, 'speechiness': 0.25, 'tempo': 110, 'valence': 1}, 
        'PEACEFUL': {'acousticness': 1, 'danceability': 0.125, 'energy': 0, 'instrumentalness': 1, 'loudness': 0, 'speechiness': 0.66, 'tempo': 60, 'valence': 0.66}, 
        'DREAMY': {'acousticness': 0.66, 'danceability': 0, 'energy': 0.25, 'instrumentalness': 0.66, 'loudness': -5, 'speechiness': 0.5, 'tempo': 85, 'valence': 0.75}
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
        
def main():
    # This is an example input that the front end will end up scraping
    songs = {0: 'Waiting for Love', 1: 'High on Life', 2: 'Homecoming'}
    artists = {0: 'Avicii', 1: 'Martin Garrix', 2: 'Kanye West'}
    genres = {0: 'EDM', 1: 'Rap', 2: 'Pop'}
    # Currently providing random selections for action and mood for testing purposes
    actions = ['WORKINGOUT', 'STUDYING', 'DRIVING', 'DANCING', 'RELAXING', 'CLEANING']
    action_choice = actions[int(random() * len(actions))]
    moods = ['ANGRY', 'ANXIOUS', 'ENERGIZED', 'AMUSED', 'MELANCHOLY', 'EMPOWERED', 'DEFIANT', 'FEARFUL', 'CHEERFUL', 'CHARMING', 'PEACEFUL', 'DREAMY']
    mood_choice = moods[int(random() * len(moods))]   
    theme = ''
    num_songs = 50

    # Send the selection of user input
    selection = audio_features(action_choice, mood_choice)
    print("Selection: <" + action_choice + ", " + mood_choice + ">")
    print(selection)

    #TODO Send songs, artists, genres, selction, theme, num_songs to elastic search team
main()
