from elasticsearch_db import ElasticsearchDB
import json
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent + '\spotify_scripts')
import SongFeatures

# Create the elasticsearch_db object
es_db = ElasticsearchDB()

# Create song index
mapping_file = os.path.dirname(os.path.realpath(__file__)) + '\song_mapping.json'
with open(mapping_file) as f: # Load the song mapping json from this directory.
    song_mapping = json.load(f)
es_db.create_index('songs', song_mapping)

# Get songList from external script
songList = SongFeatures.get_tracks_for_es()
print('Obtained song list')

# Store all songs from songList into elasticsearch
for i, song in enumerate(songList):
    r = i == (len(songList) - 1)
    es_db.store_record('songs', i, song, r)
print('Stored all songs in Elasticsearch database')

# Test to see if all songs are returned when queried
search_object = {'query': {'match_all': {}}}
results = es_db.search('songs', search_object)
for i, doc in enumerate(results['hits']['hits']):
    print(f'Hit {i+1}: {doc["_source"]["name"]}')