import './App.css';
import React from 'react';
import '../node_modules/bootstrap/dist/css/bootstrap.min.css';
import ColorPicker from './components/ColorPicker';
import ActivityButton from './components/Selector';
import APIService from './components/APIService';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faThumbsUp, faThumbsDown } from '@fortawesome/free-solid-svg-icons'

let userData = {
  favSongs: [],
  favArtists: [],
  favGenres: [],
  activities: [],
  mood: "peaceful",
  name: "Octave Playlist",
  number: 20
}

let likes = {
  songs: [],
  keys: []
}

let genres = [
  "Alternative",
  "Blues",
  "Classical",
  "Country",
  "Dance",
  "Electronic",
  "Hip-Hop",
  "Jazz",
  "Metal",
  "Pop",
  "R&B",
  "Rock"
]
let currentResponse = {}
let currentKey = []
let likesIndex = 0

let postResponsemessage = ""
let postResponse = {}
let playlistUrl = ""

function collectData() {
  //Get activities
  let activityButtons = document.getElementsByClassName("Selected");
  userData.activities = [];
  for (let i=0; i<activityButtons.length; i++) {
    userData.activities.push(activityButtons[i].id)
  }
  //Get mood
  userData.mood = document.getElementsByClassName("Mood")[0].innerHTML;

  //Make sure likes/dislikes are unselected

  likes.songs = []
  likes.keys = []

  //Send to flask
  APIService.InsertQuery(userData)
  .then((response) => openPopup(response))
  .catch(error => openPopup(error))
}

function openPopup(response) {
  if(response) {
    postResponsemessage = "Success! Connected to Flask."
    postResponse=response.result;
    saveResponse(postResponse);
    displayOutput();
  }else{
    postResponsemessage = "Error: could not connect to Flask.";
  }
  var modal = document.getElementById("myModal");
  modal.firstChild.childNodes[2].textContent = JSON.stringify(userData)
  modal.firstChild.childNodes[3].textContent = postResponsemessage
  modal.style.display = "block";
}

function saveResponse(response) {
	currentResponse = {}
	currentKey = []
	document.getElementById("moreSongsButton").childNodes[0].style.visibility = 'visible'
	for (let j = 0;  j < 3; j++) {
		document.getElementById("myResult").childNodes[0].childNodes[j].childNodes[0].style.visibility = 'visible'
		document.getElementById("like" + j).style.visibility = 'visible'
		document.getElementById("dislike" + j).style.visibility = 'visible'
	}
	var i = 0
	for (const key in postResponse) {
		currentResponse[i] = response[key]
		currentKey[i] = key
		i++
	}
	likesIndex = 0;
}

function displayOutput(){
  console.log(likesIndex)
  console.log(currentKey.length)

  //Make sure likes/dislikes are unselected
  for (let i=0; i<3; i++) {
    	document.getElementById("like" + i).classList.remove("active");
  	document.getElementById("dislike" + i).classList.remove("active");
  }


  for (let i = likesIndex; i < likesIndex + 3; i++) {
	if (i < currentKey.length) {
		document.getElementById("myResult").childNodes[0].childNodes[i%3].childNodes[0].textContent = currentResponse[i][0] + ', ' + currentResponse[i][1]
    		document.getElementById("myResult").childNodes[0].childNodes[i%3].childNodes[0].href = currentResponse[i][2]
    		likes.keys[i] = currentKey[i]
	} else {
		document.getElementById("myResult").childNodes[0].childNodes[i%3].childNodes[0].style.visibility = 'hidden'
		document.getElementById("like" + i%3).style.visibility = 'hidden'
		document.getElementById("dislike" + i%3).style.visibility = 'hidden'
	}

  }
  likesIndex += 3
  if (likesIndex > currentKey.length - 1) {
	document.getElementById("moreSongsButton").childNodes[0].style.visibility = 'hidden'
  }
}

function openPopup2(response) {
  if(response) {
    playlistUrl=response.message
  }
  closePopup("myModal")
  var modal = document.getElementById("myModal2");
  modal.firstChild.childNodes[3].href = playlistUrl;
  modal.style.display = "block";
}

function closePopup(id) {
  var modal = document.getElementById(id);
  modal.style.display = "none";
}

function setLike(i) {
  likes.songs[i + likesIndex - 3] = 1
  document.getElementById("like"+i).classList.add("active")
  document.getElementById("dislike"+i).classList.remove("active")
}
function setDislike(i) {
  likes.songs[i + likesIndex - 3] = 0
  document.getElementById("like"+i).classList.remove("active")
  document.getElementById("dislike"+i).classList.add("active")
}

function generatePlaylist() {
  for (let i = 0; i < currentKey.length; i++) {
    if (likes.songs[i] === 0) {
      delete postResponse[likes.keys[i]]
    }
  }
  postResponse['name'] = userData.name
  APIService.GetPlaylist(postResponse)
  .then((response) => openPopup2(response))
  .catch(error => openPopup(error))
}

function buildGenres(num) {
  var model = document.getElementById("FavGenres");
  var elem = model.childNodes.item(num)
  for (let i = 0; i < genres.length; i++){
      elem.innerHTML += "<option value=\"" + genres[i] + "\">" + genres[i] + "</option>";
  }
}

function min(val, min, max) {
  if (val > max) {
    return max;
  } else if (val < min) {
    return min;
  }
  return val;
}

function validate(text) {
  var i = 0;
  while (i < text.length) {
    var charCode = text.charCodeAt(i);
    if (
      charCode !== 32 &&                        // Space
      !(charCode > 47 && charCode < 58) &&     // Numbers 0-9
      !(charCode > 64 && charCode < 91) &&     // Uppercase A-Z
      !(charCode > 96 && charCode < 123)       // Lowercase a-z
      ) {
        text = text.substring(0, i) + text.substring(i+1);
    } else {
      i++;
    }
  }
  return text;
}

function clean(text) {
  
}

function App() {

  return (
    <div className="App">
      <header className="App-header">
        <img src="./octavelogo.png" alt = "logo" width="480px"/>
      </header>

      <h5 className="intro">Welcome to Octave, a custom Spotify playlist generator based on your favorite music, current activities, and moods you want to feel. To get started, tell as about yourself. What are some of your...</h5>
      
      <form id="favorites">
        <h3>Favorite Songs</h3>
        <div className = "FavSongs" id = "FavSongs">
          <input maxlength = "25" onChange={(event) => userData.favSongs[0] = validate(event.target.value)} id="favSong1"></input>
          <input maxlength = "25" onChange={(event) => userData.favSongs[1] = validate(event.target.value)} id="favSong2"></input>
          <input maxlength = "25" onChange={(event) => userData.favSongs[2] = validate(event.target.value)} id="favSong3"></input>
        </div> 

        <h3>Favorite Artists</h3>
        <div className = "FavArtists" id = "FavArtists">
          <input maxlength = "25" onChange={(event) => userData.favArtists[0] = validate(event.target.value)} id="favGenre1"></input>
          <input maxlength = "25" onChange={(event) => userData.favArtists[1] = validate(event.target.value)} id="favGenre2"></input>
          <input maxlength = "25" onChange={(event) => userData.favArtists[2] = validate(event.target.value)} id="favGenre3"></input>
        </div>
      </form>
              
        <h3>Favorite Genres</h3>
        <div className = "FavGenres" id = "FavGenres">
          <select onChange={(event) => userData.favGenres[0] = event.target.value} name="genre1" id="genre1">
            <option value="Alternative">Alternative</option>
            <option value="Blues">Blues</option>
            <option value="Classical">Classical</option>
            <option value="Country">Country</option>
            <option value="Dance">Dance</option>
            <option value="Electronic">Electronic</option>
            <option value="Hip-Hop">Hip-Hop</option>
            <option value="Jazz">Jazz</option>
            <option value="Metal">Metal</option>
            <option value="Pop">Pop</option>
            <option value="Rock">Rock</option>
          </select>

        <select onChange={(event) => userData.favGenres[1] = event.target.value} name="genre2" id="genre2">
          <option value="Alternative">Alternative</option>
            <option value="Blues">Blues</option>
            <option value="Classical">Classical</option>
            <option value="Country">Country</option>
            <option value="Dance">Dance</option>
            <option value="Electronic">Electronic</option>
            <option value="Hip-Hop">Hip-Hop</option>
            <option value="Jazz">Jazz</option>
            <option value="Metal">Metal</option>
            <option value="Pop">Pop</option>
            <option value="Rock">Rock</option>
        </select>

        <select onChange={(event) => userData.favGenres[2] = event.target.value} name="genre3" id="genre3">
          <option value="Alternative">Alternative</option>
            <option value="Blues">Blues</option>
            <option value="Classical">Classical</option>
            <option value="Country">Country</option>
            <option value="Dance">Dance</option>
            <option value="Electronic">Electronic</option>
            <option value="Hip-Hop">Hip-Hop</option>
            <option value="Jazz">Jazz</option>
            <option value="Metal">Metal</option>
            <option value="Pop">Pop</option>
            <option value="Rock">Rock</option>
          </select>
        </div>

        <div className = "ActivitySelector">
          <h2>What are you doing?</h2>
          <ActivityButton name = "Studying"/>
          <ActivityButton name = "Working out"/>
          <ActivityButton name = "Relaxing"/>
          <ActivityButton name = "Driving"/>
          <ActivityButton name = "Dancing"/>
        </div>

        <div className = "MoodSelector">
          <h2>How are you feeling?</h2>
          <div className = "Slider">
            <ColorPicker/>
          </div>
        </div>

        <ul className = "NameNum">
          <li>
            <h4>Playlist Name:</h4>
            <input maxlength = "25" onChange={(event) => userData.name = validate(event.target.value)}></input>
          </li>
          <li>
            <h4>Number of Songs(10-99):</h4>
            <input type = "number" min = "10" max = "99" onChange={(event) => userData.number = min(event.target.value, 10, 99)}></input>
          </li>
        </ul>

      <div className = "Generate">
        <button onClick={collectData}>Generate Playlist</button>
      </div>

      <div id="myModal" className="modal">
        <div className="modal-content">
          <span className="close" onClick={()=> closePopup("myModal")}>&times;</span>
          <h4>User Data</h4>
          <p></p>
          <p></p>
          <h4>Do you like these songs?</h4>
          <div id="myResult" className="result">
            <ul>
              <li><a href="test.com" target="_blank">Test1</a><div class="rating">
                <div id="like0" class = "like" onClick={() => setLike(0)}><React.Fragment><FontAwesomeIcon icon={faThumbsUp}/></React.Fragment></div>
                <div id="dislike0" class = "dislike" onClick={() => setDislike(0)}><FontAwesomeIcon icon = {faThumbsDown}/></div>
              </div></li>
              <li><a href="test.com" target="_blank">Test2</a><div class="rating">
                <div id="like1" class = "like" onClick={() => setLike(1)}><React.Fragment><FontAwesomeIcon icon={faThumbsUp}/></React.Fragment></div>
                <div id="dislike1" class = "dislike" onClick={() => setDislike(1)}><FontAwesomeIcon icon = {faThumbsDown}/></div>
              </div></li>
              <li><a href="test.com" target="_blank">Test3</a><div class="rating">
                <div id="like2" class = "like" onClick={() => setLike(2)}><React.Fragment><FontAwesomeIcon icon={faThumbsUp}/></React.Fragment></div>
                <div id="dislike2" class = "dislike" onClick={() => setDislike(2)}><FontAwesomeIcon icon = {faThumbsDown}/></div>
              </div></li>
            </ul>
          </div>
	  <div id="moreSongsButton">
	  	<button onClick={displayOutput}>Show more songs!</button>
	  </div>
          <button onClick={generatePlaylist}>Continue</button>
        </div>
      </div>

      <div id="myModal2" className="modal">
        <div className="modal-content">
          <span className="close" onClick={()=> closePopup("myModal2")}>&times;</span>
          <img src="./octavelogo.png" alt = "logo" width="240px"/>
          <h4>Enjoy your playlist!</h4>
          <a href="www.google.com" target="_blank">Click here</a>
        </div>
      </div>


    </div>
  );
}

export default App;