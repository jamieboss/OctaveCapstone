import json
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from elasticsearch_db import ElasticsearchDB

def test_create_index(test_es):
    with open('test_mapping.json') as f:
        test_mapping = json.load(f)
    test_es.create_index('tests', test_mapping)
    assert test_es.es.indices.get_mapping(index='tests')

def test_delete_index(test_es):
    test_es.delete_index('tests')
    assert True

def test_store_record(test_es):
    record_object = {'name': 'Blank Space', 'artist': 'Taylor Swift', 'album': '1989', 'mood': 0.5}
    test_es.store_record('tests', record_object)
    assert test_es.es.count(index='tests')['count'] == 1

def test_search_match(test_es):
    search_object = {'query': {'match': {'artist': 'Taylor Swift'}}}
    results = test_es.search('tests', search_object)
    assert results['hits']['hits'][0]['_source']['name'] == 'Blank Space'

def test_search_compound_query(test_es):
    search_object = {'query': {'bool': {'must': [{'match': {'artist': 'Taylor Swift'}}, {'match': {'album': '1989'}}]}}}
    results = test_es.search('tests', search_object)
    assert results['hits']['hits'][0]['_source']['name'] == 'Blank Space'

def test_search_fail(test_es):
    search_object = {'query': {'bool': {'must': [{'match': {'artist': 'Taylor Swift'}}, {'match': {'album': 'Red'}}]}}}
    results = test_es.search('tests', search_object)
    assert not results['hits']['hits']

def test_search_range(test_es):
    search_object = {'query': {'range': {'mood': {'gte': 0.4, 'lte': 0.8}}}}
    results = test_es.search('tests', search_object)
    assert results['hits']['hits'][0]['_source']['name'] == 'Blank Space'

if __name__ == '__main__':
    test_es = ElasticsearchDB()
    test_create_index(test_es)
    test_store_record(test_es)
    test_search_match(test_es)
    test_search_compound_query(test_es)
    test_search_fail(test_es)
    test_search_range(test_es)
    test_delete_index(test_es)
    print('Everything passed')
