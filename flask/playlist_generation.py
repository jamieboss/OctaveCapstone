from cgitb import reset
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from features_alter import select_features_alter

def playlist_from_input(input):
    # authorization information

    CLIENT_ID = 'f54a10c8ab084526a1df90b9c7f4f19f'
    CLIENT_SECRET = '2178e29186714432b61020743e950821'
    REDIRECT_URI = 'http://localhost'

    client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    input_features = select_features_alter(input);
    number_of_songs = input['number'];

    input_artists_id = [];
    for (artist) in input['favArtists']:
    	res = sp.search(q=artist, limit=1, offset=0, type="artist", market="US");
    	artist_id = res["artists"]["items"][0]["id"];
    	input_artists_id.append(artist_id);

    input_songs_id = [];
    for (song) in input['favSongs']:
    	res = sp.search(q=song, limit=1, offset=0, type="track", market="US");
    	song_id = res["tracks"]["items"][0]["id"];
    	input_songs_id.append(song_id);
    
    songs = sp.recommendations(seed_artists = input_artists_id, seed_genres=None, seed_tracks=input_songs_id, limit=number_of_songs, country=None, target_acousticness = input_features[0], target_danceability = input_features[1], target_energy = input_features[2], target_speechiness = input_features[3], target_tempo = input_features[4], target_valence = input_features[5]);

    return songs;