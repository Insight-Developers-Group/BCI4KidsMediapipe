import React from 'react'
import eyelogo from '../Resources/eyelogo.svg'
import girllogo from '../Resources/girllogo.svg'
import PropTypes from 'prop-types'

function ModeSwitcher(props) {

    const [trackingLabel, setTrackingLabel] = React.useState('| Face Tracking')

    function changeLabelToFaceTracking() {                  /*flips the trackingLabel state from face tracking to eye tracking and vice versa */
        setTrackingLabel(prevLabel => '| Face Tracking')
    }

    function changeLabelToEyeTracking() {
        setTrackingLabel(prevLabel => '| Eye Tracking')
    }

    return (
        <div>
            <div className='girlBgrnd' onClick={changeLabelToFaceTracking}>
                <img className='girllogo' src={girllogo} />
            </div>
            <div className='eyeBgrnd' onClick={changeLabelToEyeTracking}>
                <img className='eyelogo' src={eyelogo} />
            </div>
            <div className='trackingLabel'>
                <p className='labelContent'>{trackingLabel}</p>
            </div>
        </div>
    )
}

ModeSwitcher.propTypes = {

}

export default ModeSwitcher

