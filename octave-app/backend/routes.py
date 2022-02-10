from app import app
from random import random
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import features

@app.route('/')
def main():
    # authorization information
    CLIENT_ID = 'f54a10c8ab084526a1df90b9c7f4f19f'
    CLIENT_SECRET = '2178e29186714432b61020743e950821'
    REDIRECT_URI = 'http://localhost/'

    SCOPE = 'user-library-read'

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=SCOPE))
    # This is an example input that the front end will end up scraping
    songs = {0: 'Waiting for Love', 1: 'High on Life', 2: 'Homecoming'}
    artists = {0: 'Avicii', 1: 'Martin Garrix', 2: 'Kanye West'} # {0: '1vCWHaC5f2uS3yhpwWbIA6', 1: '60d24wfXkVzDSfLS6hyCjZ', 2: '5K4W6rqBFWDnAN6FQUkS6x'}
    genres = {0: 'EDM', 1: 'Rap', 2: 'Pop'}
    # Currently providing random selections for action and mood for testing purposes
    actions = ['WORKINGOUT', 'STUDYING', 'DRIVING', 'DANCING', 'RELAXING', 'CLEANING']
    action_choice = actions[int(random() * len(actions))]
    moods = ['ANGRY', 'ANXIOUS', 'ENERGIZED', 'AMUSED', 'MELANCHOLY', 'EMPOWERED', 'DEFIANT', 'FEARFUL', 'CHEERFUL', 'CHARMING', 'PEACEFUL', 'DREAMY']
    mood_choice = moods[int(random() * len(moods))]   
    theme = ''
    num_songs = 50

    # Send the selection of user input
    selection = features.audio_features(action_choice, mood_choice)
    return selection