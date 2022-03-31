from SpotifyOAuth import sp

id = "spotify:artist:3ApUX1o6oSz321MMECyIYd?si=9JtOb6KKSNm1boeBYvyTFg"
trackId = "spotify:track:1dGr1c8CrMLDpV6mPbImSI?si=2e466e23338e432d"
category = "party"



def categorySongs():
    playlistIds = []
    playlists = sp.category_playlists( category_id = "party", country = "US", limit = 2, offset = 0)['playlists']['items']
    for playlist in playlists:
        name = playlist['id']
        playlistIds.append(name)
    
    songIds = []
    #temporary playlist id
    id = 'spotify:playlist:37i9dQZF1DXa2PvUpywmrr?si=62d9b3c57261414f'
   #add loop to itereaate through playlistIds
    results = sp.playlist_items(id)['tracks']['items']
    for track in results:
        name = track["track"]["name"]
        songId = track["track"]["id"]
        songIds.append(songId)
        print(name)
  #songIds contains list of song ids from playlist
  #playlistIds contains a list of playlist ids,
#got stuck because I could not figure out how to get the songs from the format that the playlist ids were given in
        
def categories():
    cats = sp.categories(country="US", locale="eng", limit=20, offset=0)


categorySongs()
