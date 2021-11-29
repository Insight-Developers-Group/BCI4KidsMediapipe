import React from 'react'
import helpLogo from '../Resources/helplogo.svg';
import PropTypes from 'prop-types'

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

HelpButton.propTypes = {

}

export default HelpButton

