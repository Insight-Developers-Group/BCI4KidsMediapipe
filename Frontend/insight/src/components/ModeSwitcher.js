import React from 'react'
import eyelogo from '../Resources/eyelogo.svg'
import girllogo from '../Resources/girllogo.svg'

function ModeSwitcher(props) {

    const [trackingLabel, setTrackingLabel] = React.useState('| Face Tracking')

    function changeLabelToFaceTracking() {                  /*flips the trackingLabel state from face tracking to eye tracking and vice versa */
        setTrackingLabel(prevLabel => '| Face Tracking')
        console.log("Changed to face tracking")
    }

    function changeLabelToEyeTracking() {
        setTrackingLabel(prevLabel => '| Eye Tracking')
        console.log("Changed to eye tracking")
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

export default ModeSwitcher
