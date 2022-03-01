
import elasticsearch_db as esd
import json
import sys
sys.path.insert(1, '../spotify_scripts')
from spotify_scripts import SongFeatures

# Create the elasticsearch_db object
es_db = esd.ElasticsearchDB()

# Create song index
with open('elasticsearch/song_mapping.json') as f: # Load the song mapping json from this directory.
    song_mapping = json.load(f)
es_db.create_index('songs', song_mapping)

# Get songList from external script
songList = SongFeatures.get_tracks_for_es()

# Store all songs from songList into elasticsearch
for song in songList:
    es_db.store_record('songs', song)

# Test to see if all songs are returned when queried
search_object = {'query': {'match_all': {}}}
results = es_db.search('tests', search_object)
for i, doc in enumerate(results['hits']['hits']):
    print(f'Hit {i+1}: {doc["_source"]["name"]}')