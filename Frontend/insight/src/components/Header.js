import React from 'react'

const Header = ({text}) => {
    return (
        <div>
            <h1>{text}</h1>
        </div>
    )
}

Header.defaultProps = {
    text: 'InSight',
}

export default Header
