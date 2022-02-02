import json
from elasticsearch import Elasticsearch

def connect_elasticsearch():
    _es = None
    _es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if _es.ping():
        print('Connected!')
    else:
        print('Could not connect')
    return _es

def create_index(es_object, index_name='songs'):
    created = False
    # index settings
    mappings = {
        "mappings": {
            "members": {
                "dynamic": "strict",    # force Elasticsearch to do a strict checking of any incoming document
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
    }
    try:
        if not es_object.indices.exists(index=index_name):
            es_object.indices.create(index=index_name, mappings=mappings)
            print('Created Index')
            created = True
    except Exception as ex:
        print(str(ex))
    finally:
        return created
    
def store_record(es_object, index_name, record):
    try:
        outcome = es_object.index(index=index_name, doc_type='_doc', document=record)
    except Exception as ex:
        print('Error in indexing data')
        print(str(ex))

def search(es_object, index_name, search):
    res = es_object.search(index=index_name, body=search)

es = connect_elasticsearch()
if es is not None:
    create_index(es)
    record_object = {'name': 'Blank Space', 'artist': 'Taylor Swift', 'album': '1989'}
    store_record(es, 'songs', record_object)
    search_object = {'query': {'match': {'artist': 'Taylor Swift'}}}
    search(es, 'songs', json.dumps(search_object))