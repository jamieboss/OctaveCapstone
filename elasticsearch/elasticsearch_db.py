import json
import logging
from elasticsearch import Elasticsearch

class ElasticsearchDB:

    def __init__(self):
        self.es = Elasticsearch([{'host': 'localhost', 'port': 9200}]) # Change once we have shared elasticsearch
        #self.es = Elasticsearch("http://localhost:9200")
        logging.info(self.es.ping())

    def create_index(self, index_name, mapping):
        logging.info(f'Creating index {index_name} with the following schema:\n{json.dumps(mapping, indent=2)}')
        # ignore 400 cause by indexAlreadyExistsException when creating an index
        self.es.indices.create(index=index_name, ignore=400, body=mapping)
        
    def delete_index(self, index_name):
        logging.info(f'Deleting index {index_name}')
        self.es.indices.delete(index=index_name, ignore=[400,404])

    def store_record(self, index_name, id, doc, r):
        logging.info(f'Writing document to ES index {index_name}')
        res = self.es.index(index=index_name, id=id, document=json.dumps(doc), refresh = r)

    def search(self, index_name, query):
        res = self.es.search(index=index_name, size=10000, body=json.dumps(query))
        return res

