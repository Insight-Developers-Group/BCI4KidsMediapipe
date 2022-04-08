import React from "react";
import irisDark from "../Resources/iris-dark.svg";
import irisLight from "../Resources/iris-light.svg";
import faceDark from "../Resources/girllogo.svg";
import faceLight from "../Resources/girllogo-light.svg";
// import girllogolight from "../Resources/girllogo-light.svg";

function ModeSwitcher(props) {
    const [trackingLabel, setTrackingLabel] = React.useState("Face Tracking");
    let fullFooterClass = "footerElements";
    if (props.flipCardsMode) fullFooterClass += " footer-flipped";

    function changeLabelToFaceTracking() {
        /* flips the trackingLabel state from face tracking to eye tracking */
        setTrackingLabel("Face Tracking");
        props.changeMode("face");
        console.log("Changed to face tracking");
    }

    function changeLabelToEyeTracking() {
        /* flips the trackingLabel state from eye tracking to face tracking */
        setTrackingLabel("Eye Tracking");
        props.changeMode("eye");
        console.log("Changed to eye tracking");
    }

    function getIconColor(type) {
        /* returns the correct icon for the specified type based on the current tracking mode */
        if (type === "face") {
            if (props.mode === "eye") {
                return faceLight;
            } else {
                return faceDark;
            }
        } else {
            if (props.mode === "eye") {
                return irisDark;
            } else {
                return irisLight;
            }
        }
    }

    return (
        <div className={fullFooterClass}>
            <div
                className={"girlBgrnd " + props.mode + "-selected-face-bg"}
                onClick={changeLabelToFaceTracking}
                data-testid="girlBgrnd">
                <img
                    className="girllogo"
                    src={getIconColor("face")}
                    alt="girllogo"
                />
            </div>
            <div
                className={"eyeBgrnd " + props.mode + "-selected-eye-bg"}
                onClick={changeLabelToEyeTracking}
                data-testid="eyeBgrnd">
                <img
                    className="eyelogo"
                    src={getIconColor("eye")}
                    alt="eyelogo"
                />
            </div>
            <p className="labelContent" data-testid="para">
                {trackingLabel}
            </p>
        </div>
    );
}

export default ModeSwitcher;
