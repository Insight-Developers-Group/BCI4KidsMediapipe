import React from "react";
import helpLogo from "../Resources/helplogo.svg";
import crossIcon from "../Resources/crossicon.svg";

function HelpMenu(props) {
    return (
        <>
            <div className="help-menu-overlay" onClick={props.toggle} ></div>
            <div className="help-menu" data-testid="help-menu">
                <img
                    className="help-menu-close"
                    src={crossIcon}
                    onClick={props.toggle}
                    alt="close help menu"
                    data-testid="help-menu-overlay-close"
                />
                <img
                    className="help-menu-icon"
                    src={helpLogo}
                    alt="help menu icon"
                />
                <h1 className="help-menu-title">Help</h1>
                <div className="help-menu-content">
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed
                    do eiusmod tempor incididunt ut labore et dolore magna
                    aliqua. Ut enim ad minim veniam, quis nostrud exercitation
                    ullamco laboris nisi ut aliquip ex ea commodo consequat.
                    Duis aute irure dolor in reprehenderit in voluptate velit
                    esse cillum dolore eu fugiat nulla pariatur. Excepteur sint
                    occaecat cupidatat non proident, sunt in culpa qui officia
                    deserunt mollit anim id est laborum.
                </div>
            </div>
        </>
    );
}

export default HelpMenu;
