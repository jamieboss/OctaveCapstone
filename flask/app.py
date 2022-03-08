from flask import Flask, redirect, jsonify, request, session
from flask_cors import CORS, cross_origin
from itsdangerous import json
import requests
from search_examples import favSongs, favArtists
from Main import song_analysis

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = 'osd(99092=36&462134kjKDhuIS_d23'

@app.route('/data', methods=['POST'])
@cross_origin()
def user_query():
    input = request.get_json()
    print('REQUEST RECEIVED:')
    print(input)
    
    '''
    This call to main will send over all of the input data from the front end over to the analysis function
    '''
    #song_results = song_analysis(input)
    #return jsonify(result=song_results)

    '''
    Example: 
    This loop below iterates over each favorite song and returns its track id, name, and artist
    My spotify API is not working so these "results" are pulled from three manual hits to the API i made to get song data and I am treating it like a black box currently. 
    '''
    
    song_results = {}
    for hit in favSongs:
        track = hit["tracks"]["items"][0]
        track_id = track["id"]
        song_results[track_id] = []
        song_results[track_id].append(track["name"])
        song_results[track_id].append(track["artists"][0]["name"])
        song_results[track_id].append(track["external_urls"]["spotify"])
    print('REQUEST SENT:')
    print(song_results)
    return jsonify(result=song_results)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080", debug=True)