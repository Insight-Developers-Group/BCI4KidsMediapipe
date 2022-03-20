import React from "react";
import irisDark from "../Resources/iris-dark.svg";
import irisLight from "../Resources/iris-light.svg";
import faceDark from "../Resources/girllogo.svg";
import faceLight from "../Resources/girllogo-light.svg";
// import girllogolight from "../Resources/girllogo-light.svg";

function ModeSwitcher(props) {
    const [trackingLabel, setTrackingLabel] = React.useState("Face Tracking");

    const [eyeColor, setEyeColor] = React.useState(irisLight);
    const [faceColor, setFaceColor] = React.useState(faceDark);

    function changeLabelToFaceTracking() {
        /*flips the trackingLabel state from face tracking to eye tracking and vice versa */
        setTrackingLabel("Face Tracking");
        props.changeMode("face");
        console.log("Changed to face tracking");
        setEyeColor(irisLight);
        setFaceColor(faceDark);
    }

    function changeLabelToEyeTracking() {
        setTrackingLabel("Eye Tracking");
        props.changeMode("eye");
        console.log("Changed to eye tracking");
        setEyeColor(irisDark);
        setFaceColor(faceLight);
    }

    return (
        <div className="footerElements">
            <div
                className={"girlBgrnd " + props.mode + "-selected-face-bg"}
                onClick={changeLabelToFaceTracking}
                data-testid="girlBgrnd">
                <img className="girllogo" src={faceColor} alt="girllogo" />
            </div>
            <div
                className={"eyeBgrnd " + props.mode + "-selected-eye-bg"}
                onClick={changeLabelToEyeTracking}
                data-testid="eyeBgrnd">
                <img className="eyelogo" src={eyeColor} alt="eyelogo" />
            </div>
            <p className="labelContent" data-testid="para">
                {trackingLabel}
            </p>
        </div>
    );
}

export default ModeSwitcher;
