from flask import Flask, redirect, jsonify, request, session
from flask_cors import CORS, cross_origin
import requests
from SpotifyOAuth import sp
from song_search_examples import favSongs


app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = 'osd(99092=36&462134kjKDhuIS_d23'

@app.route('/data', methods=['POST'])
@cross_origin()
def user_query():
    print(request.get_json())
    req = request.get_json()

    '''
    Example: 
    This loop below iterates over each favorite song and returns its track id, name, and artist
    My spotify API is not working so these "results" are pulled from three manual hits to the API i made to get song data and I am treating it like a black box currently. 
    '''
    song_results = {}
    for song in favSongs: 
        track = song["tracks"]["items"][0]
        track_id = track["id"]
        song_results[track_id] = []
        song_results[track_id].append(track["name"])
        song_results[track_id].append(track["artists"][0]["name"])
        song_results[track_id].append(track["external_urls"]["spotify"])

    #TODO Replace above example with desired analysis to gather playlist

    '''
    Important! This is how song_results should be formatted in order for the front end to parse it correctly.
    song_results = {track_id_1: [song_name, song_artist, spotify_link], ... , track_id_n: [song_name, song_artist, spotify_link]}
    '''
    return jsonify(result=song_results)

@app.route('/playlist', methods=['POST'])
@cross_origin()
def playlist_query():
    print(request.get_json())
    req = request.get_json()

    
    playlistLink = "https://open.spotify.com/playlist/068wH7INPasnsH5HL8wBok"
    return jsonify(message=playlistLink)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080", debug=True)