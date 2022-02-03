import json
import logging
from elasticsearch import Elasticsearch

def connect_elasticsearch():
    _es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    logging.info(_es.ping())
    return _es

def create_index(es_object, index_name, mapping):
    logging.info(f'Creating index {index_name} with the following schema:\n{json.dumps(mapping, indent=2)}')
    es_object.indices.create(index=index_name, ignore=400, mappings=mapping)
    
def store_record(es_object, index_name, doc):
    logging.info(f'Writing document to ES index {index_name}')
    res = es_object.index(index=index_name, document=json.dumps(doc))

def search(es_object, index_name, query):
    res = es_object.search(index=index_name, body=json.dumps(query))
    return res

logging.basicConfig(level=logging.INFO)

es = connect_elasticsearch()
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
create_index(es, 'songs', song_mapping)
#print(json.dumps(es.indices.get_mapping(index='songs'), indent=1))
record_object = {'name': 'Blank Space', 'artist': 'Taylor Swift', 'album': '1989'}
store_record(es, 'songs', record_object)
#print(es.count(index='songs'))
search_object = {'query': {'match': {'artist': {'query': 'Taylor Swift'}}}}
results = search(es, 'songs', search_object)
print(results['hits']['hits'])