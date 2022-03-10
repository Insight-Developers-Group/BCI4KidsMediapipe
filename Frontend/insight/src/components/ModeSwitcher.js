import React from "react";
import eyelogo from "../Resources/eyelogo.svg";
import girllogo from "../Resources/girllogo.svg";
import girllogolight from "../Resources/girllogo-light.svg";

function ModeSwitcher(props) {
    const [trackingLabel, setTrackingLabel] = React.useState("Face Tracking");

    function changeLabelToFaceTracking() {
        /*flips the trackingLabel state from face tracking to eye tracking and vice versa */
        setTrackingLabel("Face Tracking");
        props.changeMode("face");
        console.log("Changed to face tracking");
    }

    function changeLabelToEyeTracking() {
        setTrackingLabel("Eye Tracking");
        props.changeMode("eye");
        console.log("Changed to eye tracking");
    }

    return (
        <div className="footerElements">
            <div
                className={"girlBgrnd " + props.mode + "-selected-face-bg"}
                onClick={changeLabelToFaceTracking}
                data-testid="girlBgrnd">
                <img className="girllogo" src={girllogo} alt="girllogo" />
            </div>
            <div
                className={"eyeBgrnd " + props.mode + "-selected-eye-bg"}
                onClick={changeLabelToEyeTracking}
                data-testid="eyeBgrnd">
                <img className="eyelogo" src={eyelogo} alt="eyelogo" />
            </div>
            <p className="labelContent" data-testid="para">
                {trackingLabel}
            </p>
        </div>
    );
}

export default ModeSwitcher;
