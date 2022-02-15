
import elasticsearch_db as esd
import json

es_db = esd.ElasticsearchDB() # Create the elasticsearch_db object

with open('elasticsearch/song_mapping.json') as f: # Load the song mapping json from this directory.
    song_mapping = json.load(f)