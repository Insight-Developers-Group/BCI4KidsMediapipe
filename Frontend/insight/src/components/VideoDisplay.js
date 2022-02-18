import React, { useEffect, useRef } from "react";
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
    const webcamRef = React.useRef(null);
    const [imgSrc, setimgSrc] = React.useState(null);

    // Capture a screenshot of the current webcam view and add to the imageSrc array
    const capture = React.useCallback(() => {
        const imageSrc = webcamRef.current.getScreenshot();
        setimgSrc(imageSrc);
        if (imageSrc != null) {
            // console.log("Saving image to array");
            props.stack.push(imageSrc);
        }
    }, [webcamRef, props.stack, setimgSrc]);

    // Repeatedly capture images from the webcam
    const FRAME_RATE = 34; // Sets the framerate at which images are captured from the camera
    useEffect(() => {
        const interval = setInterval(() => {
            capture();
        }, FRAME_RATE);

        return () => clearInterval(interval);
    }, [capture]);

    return (
        <div>
            <Webcam
                id="video-display"
                audio={false}
                ref={webcamRef}
                screenshotFormat="image/jpeg"
                height={720}
                width={1280}
            />
            {/* <button onClick={capture}>Capture photo</button>
      {imgSrc && (<img src={imgSrc} alt="Frame capture"/>) } */}
        </div>
    );
}

export default VideoDisplay;
