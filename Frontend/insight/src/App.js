import React from "react"
import Button from './components/Button'
import MenuButton from './components/MenuButton'
import Menu from './components/Menu'
import UploadData from './components/UploadData'
import HelpButton from './components/HelpButton'
import HelpMenu from './components/HelpMenu'
import ReloadButton from './components/ReloadButton'
import VideoDisplay from './components/VideoDisplay'
import ModeButton from './components/ModeButton'
import ModeSwitcher from './components/ModeSwitcher'
import CardStack from './components/CardStack'
import Card from './components/Card'

function App() {

  return (
    <div className="App">
      <MenuButton />
      <HelpButton />
      <ReloadButton />
      <div className="webcam-block">
        <VideoDisplay />
        <ModeSwitcher />
      </div>
      <CardStack />
      
    </div>
  );
  
}

export default App;
