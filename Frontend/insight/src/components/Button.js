import React from 'react'
import PropTypes from 'prop-types'
import HelpButton from './HelpButton.js'
import MenuButton from './MenuButton.js'
import ModeSwitcher from './ModeSwitcher.js'
import ReloadButton from './ReloadButton'
function Button(props) {
    return (
        <div>
            <MenuButton />
            <HelpButton />
            <ReloadButton />
            <ModeSwitcher />
        </div>
    )
}

Button.propTypes = {

}

export default Button

