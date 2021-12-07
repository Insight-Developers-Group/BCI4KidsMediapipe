import React, { useEffect, useRef } from 'react';

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
        console.log("error:", err);
      });
  };
  // -----------------------------------------------

    return (
        <video id="video-display" autoPlay={true} ref={videoRef}>
          <source src={getVideo()}/>
          Please enable your webcam to continue
        </video>
    )
}

export default VideoDisplay
