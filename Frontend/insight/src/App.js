import React, { useEffect, useRef } from "react";
import Button from './components/Button';
import MenuButton from './components/MenuButton';
import Menu from './components/Menu';
import UploadData from './components/UploadData';
import HelpButton from './components/HelpButton';
import HelpMenu from './components/HelpMenu';
import ReloadButton from './components/ReloadButton';
import VideoDisplay from './components/VideoDisplay';
import ModeButton from './components/ModeButton';
import ModeSwitcher from './components/ModeSwitcher';
import CardStack from './components/CardStack';
import Card from './components/Card';

function App() {

  // Following code sourced from:
  // https://itnext.io/accessing-the-webcam-with-javascript-and-react-33cbe92f49cb
  const videoRef = useRef(null);

  useEffect(() => {
    getVideo();
  }, [videoRef]);

  const getVideo = () => {
    navigator.mediaDevices
      .getUserMedia({ video: { width: 400 } })
      .then(stream => {
        let video = videoRef.current;
        video.srcObject = stream;
        video.play();
      })
      .catch(err => {
        console.error("error:", err);
      });
  };
  // -----------------------------------------------

  return (
    <div className="App">
      <p>~~~~ Test Default Text ~~~~</p>
      <MenuButton />
      <HelpButton />
      <ReloadButton />
      <video className="video-display" ref={videoRef} />
      <ModeSwitcher />
      <CardStack />
      
    </div>
  );
  
}

export default App;
