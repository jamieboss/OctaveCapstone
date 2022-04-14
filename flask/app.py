import pandas as pd
import numpy as np
from flask import Flask, redirect, jsonify, request, session
from flask_cors import CORS, cross_origin
import requests, random
from featureMaps import mood_features, action_features

import os, sys
from search_examples import favSongs, favArtists
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
#sys.path.append(parent + '\spotify_scripts')
from SpotifyOAuth import sp

sys.path.append(parent + '\elasticsearch')
#sys.path.append(parent + '/elasticsearch')

import query

sys.path.append(parent + '\spotify_scripts')
# sys.path.append(parent + '/spotify_scripts')

from TrackGeneration import artistGeneratedTracks, genreGeneratedTracks

# read in csv file with artist name and uri pairs
cwd = os.path.dirname(os.path.realpath(__file__))
script_dir = os.path.dirname(cwd)
file = 'artist-uris.csv'
artistUriDf = pd.read_csv(os.path.normcase(os.path.join(script_dir, file)), names=['name', 'uri'])

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

    numSongs = int(req['number'])

    song_results = {}
    for song in req['favSongs']:
        # sp.search(hit, type='artist', limit=1, market='ES') to search for artist via spotify
        # es.search(...) to search for artist via elastic search
        if len(song) > 0:
            matches = esQuery.query(name=song)
            if matches:
                track_id = matches[0]['uri'].split(':')[-1]
                name = matches[0]["name"]
                artist = matches[0]["artist"]
            else:
                res = sp.search('track:{}'.format(song), type='track', limit=1, market='ES')['tracks']['items'][0]
                track_id = res['id']
                name = res['name']
                artist = res['artists'][0]['name']
            if not(track_id in song_results) and numSongs > 0:
                song_results[track_id] = []
                song_results[track_id].append(name)
                song_results[track_id].append(artist)
                song_results[track_id].append("https://open.spotify.com/track/"+track_id)
                numSongs -= 1
    
    for artist1 in req['favArtists']:
        # sp.search(hit, type='artist', limit=1, market='ES') to search for artist via spotify
        # es.search(...) to search for artist via elastic search
        if len(artist1) > 0:
            matches = esQuery.query(artist=artist1)
            if (len(matches) >= 3):
                for track in random.sample(matches, 3):
                    track_id = track['uri'].split(':')[-1]
                    if not(track_id in song_results) and numSongs > 0:
                        song_results[track_id] = []
                        song_results[track_id].append(track["name"])
                        song_results[track_id].append(track["artist"])
                        song_results[track_id].append("https://open.spotify.com/track/"+track_id)
                        numSongs -= 1

    
    for activity in req['activities']:
        matchFeatures = action_features[activity.upper()]
        matches = esQuery.query(acousticness = matchFeatures['acousticness'], danceability=matchFeatures['danceability'], energy=matchFeatures['energy'], speechiness=matchFeatures['speechiness'], tempo=matchFeatures['tempo'], valence=matchFeatures['valence'])
        numActivitySongs = int(numSongs/(4*len(req['activities']))) if int(numSongs/(4*len(req['activities']))) < len(matches) else len(matches)
        for track in random.sample(matches, numActivitySongs):
            track_id = track['uri'].split(':')[-1]
            if not(track_id in song_results) and numSongs > 0:
                song_results[track_id] = []
                song_results[track_id].append(track["name"])
                song_results[track_id].append(track["artist"])
                song_results[track_id].append("https://open.spotify.com/track/"+track_id)
                numSongs -= 1

    matchFeatures = mood_features[req['mood'].upper()]
    matches = esQuery.query(acousticness = matchFeatures['acousticness'], danceability=matchFeatures['danceability'], energy=matchFeatures['energy'], speechiness=matchFeatures['speechiness'], tempo=matchFeatures['tempo'], valence=matchFeatures['valence'])
    numMoodSongs = int(numSongs/2) if int(numSongs/2) < len(matches) else len(matches)
    for track in random.sample(matches, numMoodSongs):
        track_id = track['uri'].split(':')[-1]
        if not(track_id in song_results) and numSongs > 0:
            song_results[track_id] = []
            song_results[track_id].append(track["name"])
            song_results[track_id].append(track["artist"])
            song_results[track_id].append("https://open.spotify.com/track/"+track_id)
            numSongs -= 1

    # gets a list of songs for artists related to the given favorite artists
    artist1 = artistUriDf.loc[artistUriDf['name'].str.lower() == req['favArtists'][0].lower()]['uri'].item() if len(req['favArtists']) > 0 else []
    artist2 = artistUriDf.loc[artistUriDf['name'].str.lower() == req['favArtists'][1].lower()]['uri'].item() if len(req['favArtists']) > 1 else []
    artist3 = artistUriDf.loc[artistUriDf['name'].str.lower() == req['favArtists'][2].lower()]['uri'].item() if len(req['favArtists']) > 2 else []

    artist1Songs = []
    artist2Songs = []
    artist3Songs = []
    if len(artist1) > 0:
        artist1Songs, artist1Artists = artistGeneratedTracks(artist1)
    if len(artist2) > 0:
        artist2Songs, artist2Artists = artistGeneratedTracks(artist2)
    if len(artist3) > 0:
        artist3Songs, artist3Artists = artistGeneratedTracks(artist3)

    # gets a list of songs for each given genre
    genre1Songs = genreGeneratedTracks(req['favGenres'][0])
    genre2Songs = genreGeneratedTracks(req['favGenres'][1])
    genre3Songs = genreGeneratedTracks(req['favGenres'][2])

    # list of song ids to be queried by elasticsearch
    songList = list(np.unique([*artist1Songs, *artist2Songs, *artist3Songs, *genre1Songs, *genre2Songs, *genre3Songs]))

    # INCLUDES RELATED ARTIST SONGS AND GENRES
    relatedArtistGenreNumSongs = numSongs
    for song in random.sample(songList, relatedArtistGenreNumSongs):
        track_id = song.split(':')[-1]
        matches = esQuery.query(uri=track_id)
        if matches:
            name = matches[0]["name"]
            artist = matches[0]["artist"]
        else:
            res = sp.tracks([track_id])['tracks'][0]
            name = res['name']
            artist = res['artists'][0]['name']
        if not(track_id in song_results) and numSongs > 0:
            song_results[track_id] = []
            song_results[track_id].append(name)
            song_results[track_id].append(artist)
            song_results[track_id].append("https://open.spotify.com/track/"+track_id)
            numSongs -= 1

    # below code probably will not get reached
    if numSongs > 0:
        matches = esQuery.query() # Ran out of songs for this users preferences. Get random songs to fill rest of number of songs. (Okay since we have small sized data set)
        while numSongs > 0:
            numFillSongs = numSongs
            for track in random.sample(matches, numFillSongs):
                track_id = track['uri'].split(':')[-1]
                if not(track_id in song_results) and numSongs > 0:
                    song_results[track_id] = []
                    song_results[track_id].append(track["name"])
                    song_results[track_id].append(track["artist"])
                    song_results[track_id].append("https://open.spotify.com/track/"+track_id)
                    numSongs -= 1
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
    req = request.get_json()
    print(req)
    playlist_name = 'No Name Playlist'
    if 'name' in req.keys():
        playlist_name = req.pop('name')
    #Create Playlist
    playlist = sp.user_playlist_create('3147aozeyhiw7pg45aiywambxqq4', playlist_name, True, False, 'Enjoy your playlist! - Octave')
    sp.user_playlist_add_tracks('3147aozeyhiw7pg45aiywambxqq4', playlist["id"], req.keys())
    
    playlistLink = "https://open.spotify.com/playlist/" + playlist["id"]
    print(playlistLink)
    return jsonify(message=playlistLink)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080", debug=True)