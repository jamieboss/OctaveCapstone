from asyncio.subprocess import STDOUT
from app import app
from random import random
import features
import requests
import os
from flask import Flask, redirect, url_for


@app.route('/', methods=['GET', 'POST'])
def main():
    os.environ['NO_PROXY'] = '127.0.0.1'
    #url = 'http://localhost:3000/data'
    #res = requests.get(url=url)
    #input = res.json()
    input = {
        "activities": ["RELAXING"],
        "favArtists": ["Avicii","Martin Garrix","Kanye West"],
        "favGenres": ["EDM","Rap","Pop"],
        "mood": "TIRED",
        "num_songs": 50,
        "favSongs": ["Waiting for Love","High on Life","Homecoming"]
    }

    # Send the selection of user input
    selection = {}
    selection["OUTPUT"] = features.select_audio_features(input)
    selection["INPUT"] = input
    #requests.post(url, data = selection)
    #res_data = requests.get(url=url)
    return selection
