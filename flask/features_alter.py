# Selected features that a song is given via Spotify API
SONG_FEATURES = ["acousticness", "danceability", "energy", "speechiness", "tempo", "valence"]

# All options for the action choice and its associated song features.

# acousticness, danceability, energy, speechiness, tempo, valence
action_features = {
    'WORKINGOUT': [0.125, 0.75, 1, 0.125, 135, 0.5], 
    'STUDYING': [0.5, 0.125, 0.125, 0.33, 95, 0.66], 
    'DRIVING': [0.125, 0.5, 0.5, 0.25, 125, 0.5], 
    'DANCING': [0.25, 1, 0.5, 0.25, 115, 0.75], 
    'RELAXING': [0.75, 0, 0, 0.5, 80, 1],
}

# All options for the mood choice and its associated song features.
mood_features = {
    'ANGRY': [0, 0.5, 0.875, 0.125, 150, 0.125], 
    'ANXIOUS': [0.5, 0.33, 0.125, 0, 75, 1], 
    'ENERGIZED': [0.125, 1, 1, 0.125, 145, 0.5],       
    'JOYFULL': [0.33, 0.25, 0.33, 0.5, 115, 0.75], 
    'SAD': [0.5, 0.125, 0.125, 0.25, 80, 0], 
    'PEACEFUL': [1, 0.125, 0, 0.66, 60, 0.66], 
    'TIRED': [0.66, 0, 0.25, 0.5, 85, 0.75]
}

def select_features_alter(input):

	user_mood = input['mood'];
	user_activity = input['activities'];

	user_activity = user_activity[0];

	user_mood = user_mood.upper();
	user_activity = user_activity.upper();

	user_mood_values = mood_features[user_mood];
	user_activity_values = action_features[user_activity];

	features_toReturn = sum_lists(user_mood_values, user_activity_values);
	features_toReturn = divide_list(features_toReturn, 2);
	return features_toReturn;


def sum_lists(list1, list2):
	sum_list = [];
	for (item1, item2) in zip(list1, list2):
		sum_list.append(item1+item2)

	return sum_list

def divide_list(list,n):
	ret_list = [];
	for (item) in list:
		ret_list.append(item/n)

	return ret_list
