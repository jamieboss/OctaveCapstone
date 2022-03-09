from elasticsearch_db import ElasticsearchDB

def search_results(query):
    print('------------------------------------------------------------')
    results = es_db.search('songs', query)
    if not results:
        print('No results found')
    else:
        for i, doc in enumerate(results['hits']['hits']):
            print(f'Hit {i+1}: {doc["_source"]["name"]}')

# Create the elasticsearch_db object
es_db = ElasticsearchDB()

# All songs in index
#print('All songs')
#search_results({'query': {'match_all': {}}})

# Artist name
artist = 'Justin Bieber'
print(f'\nArtist: {artist}')
search_results({'query': {'match': {'artist': artist}}})