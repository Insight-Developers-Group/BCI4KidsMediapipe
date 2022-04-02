import React from "react";

/* Component for the top-left collapsible menu */
function MenuButton(props) {
    const [isOpen, setIsOpen] = React.useState(true);
    const [menu_btn_class, setMenuBtnClass] = React.useState("menu-btn");

    function toggle() {
        /* toggle function flips the isOpen state from open to close and vice versa, then calls animate() */
        setIsOpen((prevIsOpen) => !prevIsOpen);
        animate();
    }

    function animate() {
        /* function to animate the menu button depending on isOpen state */
        setMenuBtnClass(isOpen ? "menu-btn-open" : "menu-btn");
        if (isOpen) console.log("Menu Open");
        else console.log("Menu Closed");
    }

    function switchClrBlndMode() {
        /* toggles the colorblind mode setting */
        props.changeColorBlindMode((prevMode) => !prevMode);
    }

    function switchDarkTextMode() {
        /* toggles the darken text mode setting */
        props.changeDarkTextMode((prevMode) => !prevMode);
    }

    function switchFlipCards() {
        props.changeFlipCardsMode((prevMode) => !prevMode);
    }

    return (
        <div className="menu-wrapper">
            <div className={menu_btn_class} data-testid="menu-btn">
                <div onClick={toggle} className="burger-wrapper">
                    <div className="menu-btn__burger"></div>
                </div>
                <ul className="menu-list">
                    <li>
                        <button>About</button>
                    </li>
                    <li>
                        <button onClick={switchFlipCards}>
                            Flip Response Card Locations
                        </button>
                    </li>
                    <li>
                        <button onClick={switchClrBlndMode}>
                            Enable Colorblind Mode
                        </button>
                    </li>
                    <li>
                        <button onClick={switchDarkTextMode}>
                            Darken Card Text
                        </button>
                    </li>
                </ul>
            </div>
        </div>
    );
}

export default MenuButton;
