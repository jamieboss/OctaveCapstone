from elasticsearch_db import ElasticsearchDB
import json
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent + '\spotify-scripts')
import SongFeatures

# Create the elasticsearch_db object
es_db = ElasticsearchDB()

# Create song index
with open('song_mapping.json') as f: # Load the song mapping json from this directory.
    song_mapping = json.load(f)
es_db.create_index('songs', song_mapping)

# Get songList from external script
songList = SongFeatures.get_tracks_for_es(1)
print(songList)

# Store all songs from songList into elasticsearch
for i, song in enumerate(songList):
    es_db.store_record('songs', i, song)

# Test to see if all songs are returned when queried
search_object = {'query': {'match_all': {}}}
results = es_db.search('tests', search_object)
for i, doc in enumerate(results['hits']['hits']):
    print(f'Hit {i+1}: {doc["_source"]["name"]}')