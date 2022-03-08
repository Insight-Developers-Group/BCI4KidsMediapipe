import React from 'react'
function MenuButton(props) {
    const [isOpen, setIsOpen] = React.useState(true)
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
        <div className='menu-wrapper'>
            <div className={menu_btn_class} data-testid="menu-btn">
                <div onClick={toggle} className="burger-wrapper">
                    <div className="menu-btn__burger"></div>
                </div>
                < ul >
                    <li>Upload Training Data</li>
                    <li>About</li>
                    <li>Turn Off Camera</li>
                    <li>Other</li>
                    <li>Example</li>
                    <li>Options</li>
                </ul >

            </div>
        </div>

    )
}

export default MenuButton

