import './App.css';
import React from 'react';
import '../node_modules/bootstrap/dist/css/bootstrap.min.css';
import ColorPicker from './components/ColorPicker';
import ActivityButton from './components/Selector';

function App() {

  return (
    <div className="App">
      <header className="App-header">
        <h1> Octave Capstone</h1>
        <p>Custom Spotify Playlist Generator</p>
      </header>

      <div className = "FavInput">
        <h3>Favorite Songs</h3>
        <h3>Favorite Artists</h3>
        <h3>Favorite Genres</h3>
        <input></input>
        <input></input>
        <input></input>
        <input></input>
        <input></input>
        <input></input>
        <input></input>
        <input></input>
        <input></input>
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
        <button>Generate Playlist</button>
      </div>
    </div>
  );
}

export default App;
