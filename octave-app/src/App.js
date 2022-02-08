import './App.css';
import React from 'react';
import '../node_modules/bootstrap/dist/css/bootstrap.min.css';
import ColorPicker from './components/ColorPicker';
import ActivityButton from './components/Selector';

function App() {

  return (
    <div className="App">
      <header className="App-header">
        <p>
          Octave Capstone
        </p>
      </header>

      <ul>
        <li><h2>Songs</h2></li>
        <li><h2>Artists</h2></li>
        <li><h2>Genres</h2></li>
      </ul>
      <div className = "FavInput">
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
        <ul>
          <li>anxious</li>
          <li>joyfyl</li>
          <li>energized</li>
          <li>peaceful</li>
          <li>sad</li>
          <li>tired</li>
          <li>angry</li>
        </ul>
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
