import React, { useEffect, useRef } from 'react';
import PropTypes from 'prop-types'

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
        console.error("error:", err);
      });
  };
  // -----------------------------------------------

    return (
        <video className="video-display" autoplay="true" ref={videoRef} src={getVideo}  />
    )
}

VideoDisplay.propTypes = {

}

export default VideoDisplay

