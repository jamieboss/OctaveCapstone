import json
import logging
from elasticsearch import Elasticsearch

def connect_elasticsearch():
    _es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    logging.info(_es.ping())
    return _es

def create_index(es_object, index_name, mapping):
    logging.info(f'Creating index {index_name} with the following schema:\n{json.dumps(mapping, indent=2)}')
    # ignore 400 cause by indexAlreadyExistsException when creating an index
    es_object.indices.create(index=index_name, ignore=400, body=mapping)
    
def delete_index(es_object, index_name):
    logging.info(f'Deleting index {index_name}')
    es_object.indices.delete(index=index_name, ignore=[400,404])

def store_record(es_object, index_name, doc):
    logging.info(f'Writing document to ES index {index_name}')
    res = es_object.index(index=index_name, document=json.dumps(doc), refresh = True)

def search(es_object, index_name, query):
    res = es_object.search(index=index_name, body=json.dumps(query))
    return res

def delete_index(es_object, index_name):
    logging.info(f'Deleting index {index_name}.')
    es_object.indices.delete(index_name, ignore=[400, 404])

logging.basicConfig(level=logging.INFO)

# Connecting to localhost es and creating mapping
es = connect_elasticsearch()
delete_index(es, 'songs')
song_mapping = {
    "mappings": {
        "properties": {
            "name": {
                "type": "text"
            },
            "artist": {
                "type": "text"
            },
            "album": {
                "type": "text"
            },
            "mood": {
                "type": "double"
            },
        }
    }
}
# Creating Index and Record
create_index(es, 'songs', song_mapping)
print(json.dumps(es.indices.get_mapping(index='songs'), indent=1))
record_object = {'name': 'Blank Space', 'artist': 'Taylor Swift', 'album': '1989', 'mood': 0.5}
store_record(es, 'songs', record_object)
print(es.count(index='songs'))

# Searching for records
# Search for artist name
search_object = {'query': {'match': {'artist': 'Taylor Swift'}}}
results = search(es, 'songs', search_object)
for i, doc in enumerate(results['hits']['hits']):
    print(f'Hit {i+1}: {doc["_source"]["name"]}')

# Search for artist and album name (compound query)
search_object = {'query': {'bool': {'must': [{'match': {'artist': 'Taylor Swift'}}, {'match': {'album': '1989'}}]}}}
results = search(es, 'songs', search_object)
for i, doc in enumerate(results['hits']['hits']):
    print(f'Hit {i+1}: {doc["_source"]["name"]}, {doc["_source"]["album"]}')

search_object = {'query': {'bool': {'must': [{'match': {'artist': 'Taylor Swift'}}, {'match': {'album': 'Red'}}]}}}
results = search(es, 'songs', search_object)
if not results['hits']['hits']:
    print('No matches found')
for i, doc in enumerate(results['hits']['hits']):
    print(f'Hit {i+1}: {doc["_source"]["name"]}, {doc["_source"]["album"]}')

# Search for range
search_object = {'query': {'range': {'mood': {'gte': 0.6, 'lte': 0.8}}}}
results = search(es, 'songs', search_object)
if not results['hits']['hits']:
    print('No matches found')
for i, doc in enumerate(results['hits']['hits']):
    print(f'Hit {i+1}: {doc["_source"]["name"]}, {doc["_source"]["mood"]}')

# Deleting index
delete_index(es, 'songs')

