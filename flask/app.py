from flask import Flask, redirect, jsonify, request, session
from flask_cors import CORS, cross_origin
import requests, random
from featureMaps import mood_features, action_features

from SpotifyOAuth import sp

import os, sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
#sys.path.append(parent + '\elasticsearch')
sys.path.append(parent + '/elasticsearch')
import query

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = 'osd(99092=36&462134kjKDhuIS_d23'

@app.route('/data', methods=['POST'])
@cross_origin()
def user_query():
    req = request.get_json()
    print('REQUEST RECEIVED:')
    print(req)

    esQuery = query.Query()

    song_results = {}
    for song in req['favSongs']:
        # sp.search(hit, type='artist', limit=1, market='ES') to search for artist via spotify
        # es.search(...) to search for artist via elastic search
        if len(song) > 0:
            matches = esQuery.query(name=song)
            if matches:
                track_id = matches[0]['uri'].split(':')[-1]
                song_results[track_id] = []
                song_results[track_id].append(matches[0]["name"])
                song_results[track_id].append(matches[0]["artist"])
                song_results[track_id].append("https://open.spotify.com/track/"+track_id)

    for artist1 in req['favArtists']:
        # sp.search(hit, type='artist', limit=1, market='ES') to search for artist via spotify
        # es.search(...) to search for artist via elastic search
        if len(artist1) > 0:
            matches = esQuery.query(artist=artist1)
            for track in random.sample(matches[:25], 3):
                track_id = track['uri'].split(':')[-1]
                song_results[track_id] = []
                song_results[track_id].append(track["name"])
                song_results[track_id].append(track["artist"])
                song_results[track_id].append("https://open.spotify.com/track/"+track_id)
    
    for activity in req['activities']:
        matchFeatures = action_features[activity.upper()]
        matches = esQuery.query(acousticness = matchFeatures['acousticness'], danceability=matchFeatures['danceability'], energy=matchFeatures['energy'], speechiness=matchFeatures['speechiness'], tempo=matchFeatures['tempo'], valence=matchFeatures['valence'])
        for track in random.sample(matches, 5):
                track_id = track['uri'].split(':')[-1]
                song_results[track_id] = []
                song_results[track_id].append(track["name"])
                song_results[track_id].append(track["artist"])
                song_results[track_id].append("https://open.spotify.com/track/"+track_id)

    matchFeatures = mood_features[req['mood'].upper()]
    matches = esQuery.query(acousticness = matchFeatures['acousticness'], danceability=matchFeatures['danceability'], energy=matchFeatures['energy'], speechiness=matchFeatures['speechiness'], tempo=matchFeatures['tempo'], valence=matchFeatures['valence'])
    for track in random.sample(matches, 5):
                track_id = track['uri'].split(':')[-1]
                song_results[track_id] = []
                song_results[track_id].append(track["name"])
                song_results[track_id].append(track["artist"])
                song_results[track_id].append("https://open.spotify.com/track/"+track_id)
    
    '''
    Important! This is how song_results should be formatted in order for the front end to parse it correctly.
    song_results = {track_id_1: [song_name, song_artist, spotify_link], ... , track_id_n: [song_name, song_artist, spotify_link]}
    '''
    print('REQUEST SENT:')
    print(song_results)
    return jsonify(result=song_results)

@app.route('/playlist', methods=['POST'])
@cross_origin()
def playlist_query():
    print("RECIEVED:")
    print(request.get_json().keys())

    #Create Playlist
    playlist = sp.user_playlist_create('3147aozeyhiw7pg45aiywambxqq4', 'Test Playlist', True, False, 'Adding 0-3 songs')
    sp.user_playlist_add_tracks('3147aozeyhiw7pg45aiywambxqq4', playlist["id"], request.get_json().keys())
    
    playlistLink = "https://open.spotify.com/playlist/" + playlist["id"]
    return jsonify(message=playlistLink)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080", debug=True)