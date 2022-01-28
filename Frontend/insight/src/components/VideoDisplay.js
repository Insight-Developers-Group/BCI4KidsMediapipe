import React, { useEffect, useRef } from 'react';
import Webcam from "react-webcam";

// const videoDisplay = document.getElementById("video-display");
// if (window.visualViewport.height - videoDisplay.style.height - 80 >
//     window.visualViewport.width - videoDisplay.style.width - 32) {
//   videoDisplay.style.height = '100%';
//   videoDisplay.style.width = '0';
// } else {
//   videoDisplay.style.height = '0';
//   videoDisplay.style.width = '100%';
// }

// Component to display webcam view to the screen along with placeholder when camera is not accessible
function VideoDisplay(props) {

  var handleSuccess = function(stream) {
    const options = {mimeType: 'video/webm'}
    const recordedChunks = [];
    const mediaRecorder = new MediaRecorder(stream, options);

    mediaRecorder.addEventListener('dataavailable', function(e) {
      console.log("Data saved: " + e.data);
      if (e.data.size > 0) {
        recordedChunks.push(e.data);
      }
    });
  }

  // Following code sourced from:
  // https://itnext.io/accessing-the-webcam-with-javascript-and-react-33cbe92f49cb
  const videoRef = useRef(null);

  useEffect(() => {
    getVideo();
  }, [videoRef]);

  const getVideo = () => {
    navigator.mediaDevices
      .getUserMedia({ video: true })
      .then(stream => {
        let video = videoRef.current;
        video.srcObject = stream;
        video.play();
      })
      .catch(err => {
        console.log("error:", err);
      });
  };
  // -----------------------------------------------

  navigator.mediaDevices.getUserMedia({ video: true })
    .then(handleSuccess);

    const webcamRef = React.useRef(null);
    const [imgSrc, setimgSrc] = React.useState(null);
    
    const capture = React.useCallback(
      () => {
        const imageSrc = webcamRef.current.getScreenshot();
        setimgSrc(imageSrc);
    
      },[webcamRef,setimgSrc]
    );

  return (
    <div>
      <Webcam
        id="video-display"
        audio={false}
        height={720}
        width={1280}
        ref={webcamRef}
        screenshotFormat="image/jpeg" />
      <button onClick={capture}>Capture photo</button>
      {imgSrc && (<img src={imgSrc} alt="Frame capture"/>) }
    </div>

    // <video id="video-display" autoPlay={true} ref={videoRef}>
    //   <source src={getVideo()} data-testid='video-display' />
    //   Please enable your webcam to continue
    // </video>
  )
}

export default VideoDisplay
