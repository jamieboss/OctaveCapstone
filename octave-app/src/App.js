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

const getSong = (event, i)=>{
  userData.favSongs[i] = event.target.value;
}

const getArtist = (event, i)=>{
  userData.favArtists[i] = event.target.value;
}

const getGenre = (event, i)=>{
  userData.favGenres[i] = event.target.value;
}

const getTheme = (event) => {
  userData.theme = event.target.value;
}

const getNum = (event) => {
  userData.number = parseInt(event.target.value);
  if (!userData.number) {
    userData.number = 20;
  }
}

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

function displayOutput(){
  var list_str = '<ul>'
  for (const key in postResponse) {
    list_str += '<li><a href="' + postResponse[key][2] + ' " target="_blank">'+ postResponse[key][0] + ', ' + postResponse[key][1] + '</a></li>';
  }
  list_str += '</ul>'
  document.getElementById("myResult").innerHTML = list_str;
}

function openPopup(response) {
  if(response) {
    postResponsemessage = "Success!"
    postResponse=response.result;
  }else{
    postResponsemessage = "Error: could not connect to Flask";
  }
  var modal = document.getElementById("myModal");
  modal.firstChild.childNodes[2].textContent = JSON.stringify(userData)
  modal.firstChild.childNodes[3].textContent = postResponsemessage
  displayOutput();
  modal.style.display = "block";
}

function closePopup() {
  var modal = document.getElementById("myModal");
  modal.style.display = "none";
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
        <input onChange={(val) => getSong(val, 0)}></input>
        <input onChange={(val) => getArtist(val, 0)}></input>
        <input onChange={(val) => getGenre(val, 0)}></input>
        <input onChange={(val) => getSong(val, 1)}></input>
        <input onChange={(val) => getArtist(val, 1)}></input>
        <input onChange={(val) => getGenre(val, 1)}></input>
        <input onChange={(val) => getSong(val, 2)}></input>
        <input onChange={(val) => getArtist(val, 2)}></input>
        <input onChange={(val) => getGenre(val, 2)}></input>
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

      <h4>Add a specific theme:</h4>
      <input onChange={(val) => getTheme(val)}></input>
      <h4>Number of songs:</h4>
      <input onChange={(val) => getNum(val)}></input>

      <div className = "Generate">
        <button onClick={collectData}>Generate Playlist</button>
      </div>

      <div id="myModal" className="modal">
        <div className="modal-content">
          <span className="close" onClick={closePopup}>&times;</span>
          <h4>User Data</h4>
          <p></p>
          <p></p>
          {/* <a href="www.google.com" target="_blank">Playlist</a> */}
          <div id="myResult" className="result"></div>
        </div>
      </div>


    </div>
  );
}

export default App;
