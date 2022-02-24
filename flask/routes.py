from asyncio.subprocess import STDOUT
from app import app
from random import random
import features
import requests
import os
from flask import Flask, redirect, url_for
from flask_cors import cross_origin

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
        "number": 50,
        "favSongs": ["Waiting for Love","High on Life","Homecoming"],
        "theme": ""
    }

    # Send the selection of user input
    selection = {}
    #The output is based off my simple calculation of averages based on song features
    #Logan, Mulan, Kevin, and Grace will produce the more efficient results. This is just for placeholders
    selection["OUTPUT"] = features.select_audio_features(input)
    selection["INPUT"] = input
    #requests.post(url, data = selection)
    #res_data = requests.get(url=url)
    return selection
