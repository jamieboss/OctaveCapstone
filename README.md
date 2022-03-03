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
   - Ensure you have ran: pip install spotipy, pip install elasticsearch, pip install numpy, pip install pandas
   - Run the python file elasticsearch/populate_elasticsearch.py 
   - This will populate 10,000 songs onto your local elasticsearch and it may take a while.
   - To actually query songs in the code, you should only have to start elasticsearch (#3), then run the query code.


## Running the Web Application
In another new command terminal...
`cd octave-app`  
`npm start`
The Octave Application will now be online at 'localhost:3000'
