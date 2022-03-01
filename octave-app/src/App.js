import './App.css';
import React from 'react';
import '../node_modules/bootstrap/dist/css/bootstrap.min.css';
import ColorPicker from './components/ColorPicker';
import ActivityButton from './components/Selector';
import APIService from './components/APIService';

let userData = {
  favSongs: [],
  favArtists: [],
  favGenres: [],
  activities: [],
  mood: "peaceful",
  theme: " ",
  number: 20
}

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

  //Send to flask
  APIService.InsertQuery(userData)
  .then((response) => openPopup(response))
  .catch(error => openPopup(error))
}

function openPopup(response) {
  if(response) {
    postResponsemessage = "Success! Connected to Flask."
    postResponse=response.result;
    displayOutput();
  }else{
    postResponsemessage = "Error: could not connect to Flask.";
  }
  var modal = document.getElementById("myModal");
  modal.firstChild.childNodes[2].textContent = JSON.stringify(userData)
  modal.firstChild.childNodes[3].textContent = postResponsemessage
  modal.style.display = "block";
}

function displayOutput(){
  var list_str = '<ul>'
  for (const key in postResponse) {
    list_str += '<li><a href="' + postResponse[key][2] + ' " target="_blank">'+ postResponse[key][0] + ', ' + postResponse[key][1] + '</a><p>Test</p></li>';
  }
  list_str += '</ul>'
  document.getElementById("myResult").innerHTML = list_str;
}

function openPopup2(response) {
  if(response) {
    playlistUrl=response.message
  }
  closePopup("myModal")
  var modal = document.getElementById("myModal2");
  modal.firstChild.childNodes[2].href = playlistUrl;
  modal.style.display = "block";
}

function closePopup(id) {
  var modal = document.getElementById(id);
  modal.style.display = "none";
}

function generatePlaylist() {
  APIService.GetPlaylist(userData)
  .then((response) => openPopup2(response))
  .catch(error => openPopup(error))
}

function App() {

  return (
    <div className="App">
      <header className="App-header">
        <img src="./octavelogo.png" alt = "logo" width="480px"/>
      </header>

      <h5 className="intro">Welcome to Octave, a custom Spotify playlist generator based on your favorite music, current activities, and moods you want to feel. To get started, tell as about yourself. What are some of your...</h5>
      <div className = "FavInput">
        <h3>Favorite Songs</h3>
        <h3>Favorite Artists</h3>
        <h3>Favorite Genres</h3>
        <input onChange={(event) => userData.favSongs[0] = event.target.value}></input>
        <input onChange={(event) => userData.favArtists[0] = event.target.value}></input>
        <input onChange={(event) => userData.favGenres[0] = event.target.value}></input>
        <input onChange={(event) => userData.favSongs[1] = event.target.value}></input>
        <input onChange={(event) => userData.favArtists[1] = event.target.value}></input>
        <input onChange={(event) => userData.favGenres[1] = event.target.value}></input>
        <input onChange={(event) => userData.favSongs[2] = event.target.value}></input>
        <input onChange={(event) => userData.favArtists[2] = event.target.value}></input>
        <input onChange={(event) => userData.favGenres[2] = event.target.value}></input>
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

      <ul className = "ThemeNum">
        <li>
        <h4>Add a specific theme:</h4>
        <input onChange={(event) => userData.theme = event.target.value}></input>
        </li>
        <li>
        <h4>Number of songs:</h4>
        <input onChange={(event) => userData.number = parseInt(event.target.value)}></input>
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
          <div id="myResult" className="result"></div>
          <button onClick={generatePlaylist}>Continue</button>
        </div>
      </div>

      <div id="myModal2" className="modal">
        <div className="modal-content">
          <span className="close" onClick={()=> closePopup("myModal2")}>&times;</span>
          <img src="./octavelogo.png" alt = "logo" width="240px"/>
          <h4>Enjoy your playlist!</h4>
          <a href="www.google.com" target="_blank">Playlist</a>
        </div>
      </div>


    </div>
  );
}

export default App;
