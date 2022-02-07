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
        }
    }
}
# Creating Index and Record
create_index(es, 'songs', song_mapping)
print(json.dumps(es.indices.get_mapping(index='songs'), indent=1))
record_object = {'name': 'Blank Space', 'artist': 'Taylor Swift', 'album': '1989'}
store_record(es, 'songs', record_object)
print(es.count(index='songs'))

# Searching for records
search_object = {'query': {'match': {'artist': {'query': 'Taylor Swift'}}}}
results = search(es, 'songs', search_object)
for i in range(len(results['hits']['hits'])):
    print(results['hits']['hits'][i]['_source']['name'])

# Deleting index
delete_index(es, 'songs')

