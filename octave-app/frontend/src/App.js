import './App.css';
import React from 'react';
import '../node_modules/bootstrap/dist/css/bootstrap.min.css';
import ColorPicker from './components/ColorPicker';
import ActivityButton from './components/Selector';

let userData = {
  favSongs: [],
  favArtists: [],
  favGenres: [],
  activities: [],
  mood: "peaceful",
}

const getSong = (event, i)=>{
  userData.favSongs[i] = event.target.value;
}

const getArtist = (event, i)=>{
  userData.favArtists[i] = event.target.value;
}

const getGenre = (event, i)=>{
  userData.favGenres[i] = event.target.value;
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

  //Display pop-up
  var modal = document.getElementById("myModal");
  modal.firstChild.childNodes[2].textContent = JSON.stringify(userData)
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
        <h1>Octave</h1>
        <p>Custom Spotify Playlist Generator</p>
      </header>

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

      <div className = "Generate">
        <button onClick={collectData}>Generate Playlist</button>
      </div>

      <div id="myModal" className="modal">
        <div className="modal-content">
          <span className="close" onClick={closePopup}>&times;</span>
          <h4>User Data</h4>
          <p></p>
        </div>
      </div>
      
    </div>
  );
}

export default App;