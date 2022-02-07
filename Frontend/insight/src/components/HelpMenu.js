import React from 'react'
import helpLogo from "../Resources/helplogo.svg";
import crossIcon from "../Resources/crossicon.svg";

function HelpMenu(props) {
    return (
        <div>
            <div className="help-menu-overlay" onClick={props.toggle}></div>
            <div className="help-menu">
                <img className='help-menu-close' src={crossIcon} onClick={props.toggle} alt='close help menu' />
                <img className="help-menu-icon" src={helpLogo} alt="help menu icon" />
                <h1 className='help-menu-title'>Help</h1>
                <div className='help-menu-content'>

                </div>
            </div>
        </div>
    );
}

export default HelpMenu

