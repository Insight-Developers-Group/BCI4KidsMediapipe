import React from "react";
import reloadIcon from "../Resources/reloadlogo.svg";

function ReloadButton(props) {
    const [, setIsClicked] = React.useState(false);

    function toggle() {
        /*Flips the isClicked state for reload button from true to false and vice versa */
        setIsClicked((prevIsClicked) => !prevIsClicked);
        console.log("Reloaded");
    }

    return (
        <div
            className="reloadIconBgrnd"
            onClick={toggle}
            data-testid="reloadIconBgrnd">
            <img className="reload-icon" src={reloadIcon} alt="reload-icon" />
        </div>
    );
}

export default ReloadButton;
