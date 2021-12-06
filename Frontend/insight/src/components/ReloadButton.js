import React from 'react'
import PropTypes from 'prop-types'
import reloadIcon from '../Resources/reloadlogo.svg'

function ReloadButton(props) {

    const [isClicked, setIsClicked] = React.useState(false)

    function toggle() {                                     /*Flips the isClicked state for reload button from true to false and vice versa */
        setIsClicked(prevIsClicked => !prevIsClicked)
        console.log("Reloaded")
    }

    return (
        <div className="reloadIconBgrnd" onClick={toggle} >
            <img className="reload-icon" src={reloadIcon} alt='Reload' />
        </div>
    )
}

ReloadButton.propTypes = {

}

export default ReloadButton

