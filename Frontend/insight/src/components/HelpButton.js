import React, { useEffect } from "react";
import helpLogo from "../Resources/helplogo.svg";
import HelpMenu from "./HelpMenu";

function HelpButton(props) {
    const [isOpen, setisOpen] = React.useState(false);

    const toggle = () => {
        setisOpen((prevIsOpen) => !prevIsOpen);
    };

    return (
        <>
            <div
                className="helpIconBgrnd"
                onClick={toggle}
                data-testid="helpIconBgrnd">
                <img className="help-icon" src={helpLogo} alt="help-icon" />
            </div>
            {isOpen && <HelpMenu toggle={toggle} />}
        </>
    );
}

export default HelpButton;
