import React, { useEffect } from "react";
import MenuButton from "./components/MenuButton";
import HelpButton from "./components/HelpButton";
import VideoDisplay from "./components/VideoDisplay";
import ModeSwitcher from "./components/ModeSwitcher";
import CardStack from "./components/CardStack";
import SampleClient from "./components/SampleClient";
import ErrorResponse from "./components/ErrorResponse";
import { useState } from "react";

function App() {

    const [ socket, setSocket ] = useState(null);

    useEffect(() => {
        setSocket(new WebSocket("ws://127.0.0.1:8765/"));
    }, [])

    // The imageStack array will contain images captured from the user's webcam
    // Images will be constantly added through the VideoDisplay component
    // Images will be sent through a websocket using the SampleClient component and the imageStack array will be cleared
    const imageStack = [];
    const [trackingMode, setTrackingMode] = React.useState("face");

    // States for current saved responses in the system
    let [first_card, setFirstCard] = React.useState("card_none");
    let [second_card, setSecondCard] = React.useState("card_none");

    // Variable that holds new responses from the backend to be used in updating cards
    let [response, setResponse] = React.useState("");

    // Variable that holds error response messages
    const [message, setMessage] = useState("");

    // Variables for switching user settings
    const [clrblindMode, setClrBlindMode] = React.useState(false); // Enables/disables colorblind mode
    const [darkTextMode, setDarkTextMode] = React.useState(false);
    const [flipCardsMode, setFlipCardsMode] = React.useState(false);

    return (
        <div className="App">
            <MenuButton
                colorBlindMode={clrblindMode}
                changeColorBlindMode={setClrBlindMode}
                changeDarkTextMode={setDarkTextMode}
                changeFlipCardsMode={setFlipCardsMode}
            />
            <HelpButton />
            <div className="webcam-block">
                <VideoDisplay stack={imageStack} />
                <ModeSwitcher
                    mode={trackingMode}
                    changeMode={setTrackingMode}
                    flipCardsMode={flipCardsMode}
                />
            </div>
            <CardStack
                response={response}
                setResponse={setResponse}
                firstCard={first_card}
                setFirstCard={setFirstCard}
                secondCard={second_card}
                setSecondCard={setSecondCard}
                colorBlindMode={clrblindMode}
                darkTextMode={darkTextMode}
                flipCardsMode={flipCardsMode}
            />
            <ErrorResponse msg={message} />
            <SampleClient
                socket={socket}
                stack={imageStack}
                mode={trackingMode}
                response={response}
                setResponse={setResponse}
                changeMessage={setMessage}
            />
        </div>
    );
}

export default App;
