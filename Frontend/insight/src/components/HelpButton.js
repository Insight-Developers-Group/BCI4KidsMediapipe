import React from 'react'
import helpLogo from '../Resources/helplogo.svg';

function HelpButton(props) {

    const [isOpen, setisOpen] = React.useState(false)

    function toggle() {
        setisOpen(prevIsOpen => !isOpen)
        if (isOpen)
            console.log("Help Open")
        else
            console.log("Help Closed")
    }

    return (
        <div className="helpIconBgrnd" onClick={toggle}>
            <img className="help-icon" src={helpLogo} alt='Help' />
        </div>
    )
}

export default HelpButton

