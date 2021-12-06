import React from 'react'
import PropTypes from 'prop-types'
function MenuButton(props) {
    const [isOpen, setIsOpen] = React.useState(false)
    const [menu_btn_class, setMenuBtnClass] = React.useState("menu-btn")

    function toggle() {                         /*toggle function flips the isOpen state from open to close and vice versa, then calls animate()*/
        setIsOpen(prevIsOpen => !prevIsOpen)
        animate()
    }

    function animate() {                                            /*function to animate the menu button depending on isOpen state */
        setMenuBtnClass(isOpen ? "menu-btn-open" : "menu-btn")
        if (isOpen)
            console.log("Menu Open")
        else
            console.log("Menu Closed")
    }

    return (
        <div className={menu_btn_class} onClick={toggle}>
            <div className="menu-btn__burger"></div>
        </div>
    )
}

MenuButton.propTypes = {

}

export default MenuButton

