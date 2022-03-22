# This is the README for Team Octave's Capstone Project.

## Requirements 
At the end of the project, we'll need to list our requirements needed for the application
i.e
`pip install spotipy`
`pip install elasticsearch`
`pip install numpy`
`pip install pandas`


## Opening the Flask Back-End Port
`cd flask`
`py -m flask run`

## Starting up ElasticSearch
In a new command terminal...
1. Download Elasticsearch if you have not already: https://www.elastic.co/guide/en/elasticsearch/reference/current/zip-windows.html
2. In a terminal window, `cd` to elasticsearch directory you just downloaded
3. Run `.\bin\elasticsearch`
4. To load the 10,000 songs into elasticsearch on your local (should only need to be done 1 time):
   - Ensure you have elasticsearch running (#3)
   - Ensure you have ran: pip install spotipy, pip install elasticsearch==7.17.0, pip install numpy, pip install pandas
   - Run the python file elasticsearch/populate_elasticsearch.py 
   - This will populate 10,000 songs onto your local elasticsearch and it may take a while.
   - To actually query songs in the code, you should only have to start elasticsearch (#3), then run the query code.
5. To easily query songs:
   - Find a way to import query.py. If you are in a different directory, this may require something similar to what is in populate_elasticsearch.py (for some reason,   python has a hard time importing classes/functions from different directories)
   - Once imported, just instaniate the Query class ( <variable_name> = Query() )
   - <variable_name>.query(<parameters>)
   - Just include <song_feature> = <value> as a parameter for each song feature you are querying.
   - e.g.: <variable_name>.query(artist='Justin Bieber', name='Love Yourself')
   - NOTE: For all song features that are numbers you need to use <song_feature> = [<from>, <to>]. i.e. it uses an array of 2 numbers as the range. If you want a specific value, use that value for the lower and upper value of the range.
   - e.g.: <variable_name>.query(valence=[0.513, 0.513], danceability=[0.3, 0.6])
   - You can include as many or as little song features in the parameters as you want.
   - It will return an array of tracks as dictionaries with the results.

## Running the Web Application
In another new command terminal...
`cd octave-app`  
`npm start`
The Octave Application will now be online at 'localhost:3000'
