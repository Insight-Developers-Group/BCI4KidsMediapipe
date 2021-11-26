import React from 'react'
import PropTypes from 'prop-types'

function VideoDisplay(props) {
    return (
        <video autoplay="true" ref={props.ref} src={props.function}  />
    )
}

VideoDisplay.propTypes = {

}

export default VideoDisplay

