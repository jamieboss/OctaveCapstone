from elasticsearch_db import ElasticsearchDB

class Query:
    def __init__(self):
        self.es_db = ElasticsearchDB()

    def query(self, name = '', artist = '', uri = '', danceability = [0, 1], energy = [0, 1], loudness = [-60, 0], speechiness = [0, 1], acousticness = [0, 1], instrumentalness = [0, 1], valence = [0, 1], tempo = [0, 1015]):
        items = []
        if name != '':
            items.append({'match': {'name': {'query': name, 'operator': 'AND'}}})
        if artist != '':
            items.append({'match': {'artist': {'query': artist, 'operator': 'AND'}}})
        if uri != '':
            items.append({'match': {'uri': {'query': uri}}})
        if danceability != [0, 1]:
            items.append({'range': {'danceability': {'lte': danceability[1], 'gte': danceability[0]}}})
        if energy != [0, 1]:
            items.append({'range': {'energy': {'lte': energy[1], 'gte': energy[0]}}})
        if loudness != [-60, 0]:
            items.append({'range': {'loudness': {'lte': loudness[1], 'gte': loudness[0]}}})
        if speechiness != [0, 1]:
            items.append({'range': {'speechiness': {'lte': speechiness[1], 'gte': speechiness[0]}}})
        if acousticness != [0, 1]:
            items.append({'range': {'acousticness': {'lte': acousticness[1], 'gte': acousticness[0]}}})
        if instrumentalness != [0, 1]:
            items.append({'range': {'instrumentalness': {'lte': instrumentalness[1], 'gte': instrumentalness[0]}}})
        if valence != [0, 1]:
            items.append({'range': {'valence': {'lte': valence[1], 'gte': valence[0]}}})
        if tempo != [0, 1015]:
            items.append({'range': {'tempo': {'lte': tempo[1], 'gte': tempo[0]}}})

        combined_query ={'query':
                            {'bool':
                                {'must':
                                    items
                                }
                            }
                        }

        tracks = []
        results = self.es_db.search('songs', combined_query)
        if results:
            for i, doc in enumerate(results['hits']['hits']):
                track = {}
                track['name'] = doc["_source"]["name"]
                track['artist'] = doc["_source"]["artist"]
                track['uri'] = doc["_source"]["uri"]
                track['danceability'] = doc["_source"]["danceability"]
                track['energy'] = doc["_source"]["energy"]
                track['loudness'] = doc["_source"]["loudness"]
                track['speechiness'] = doc["_source"]["speechiness"]
                track['acousticness'] = doc["_source"]["acousticness"]
                track['instrumentalness'] = doc["_source"]["instrumentalness"]
                track['valence'] = doc["_source"]["valence"]
                track['tempo'] = doc["_source"]["tempo"]
                tracks.append(track)
        return tracks
# queries = Query()

# tracks = queries.query(artist='Justin Bieber', name='Love Yourself')
# for track in tracks:
#     print(track)