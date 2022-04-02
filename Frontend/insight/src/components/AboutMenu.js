import React from "react";
import helpLogo from "../Resources/helplogo.svg";
import crossIcon from "../Resources/crossicon.svg";

function AboutMenu(props) {
    return (
        <>
            <div className="about-menu-overlay" onClick={props.toggle}></div>
            <div className="about-menu">
                <img
                    className="about-menu-close"
                    src={crossIcon}
                    onClick={props.toggle}
                    alt="close about menu"
                />
                <img
                    className="about-menu-icon"
                    src={helpLogo}
                    alt="about menu icon"
                />
                <h1 className="about-menu-title">About Us</h1>
                <div className="about-menu-content">
                    Hi! We're the InSight team, a group of students from the
                    University of Calgary working together with BCI4Kids Calgary
                    to help kids better communicate with those around them.
                    Developed over the course of the CPSC 594 class, this
                    application uses machine learning and computer vision to
                    detect responses to questions based on a user's body
                    language.
                </div>
            </div>
        </>
    );
}

export default AboutMenu;
