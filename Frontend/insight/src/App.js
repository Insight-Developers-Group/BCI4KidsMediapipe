import React from "react";
import MenuButton from "./components/MenuButton";
//import Menu from './components/Menu'
import HelpButton from "./components/HelpButton";
//import HelpMenu from './components/HelpMenu'
import ReloadButton from "./components/ReloadButton";
import VideoDisplay from "./components/VideoDisplay";
//import ModeButton from './components/ModeButton'
import ModeSwitcher from "./components/ModeSwitcher";
import CardStack from "./components/CardStack";
import Client from "./components/Client";
import TestComponent from "./components/TestComponent";

function App() {
    // The imageStack array will contain images captured from the user's webcam
    // Images will be constantly added through the VideoDisplay component
    // Images will be sent through a websocket using the SampleClient component and the imageStack array will be cleared
    const imageStack = [];
    const [trackingMode, setTrackingMode] = React.useState("face");
    const [message, setMessage] = React.useState();
    const [socketState, setSocketState] = React.useState(false);

    // States for current saved responses in the system
    let [first_card, setFirstCard] = React.useState("card_none");
    let [second_card, setSecondCard] = React.useState("card_none");

    // Variable that holds new responses from the backend to be used in updating cards
    let [response, setResponse] = React.useState("");

    // Variables for switching user settings
    const [clrblindMode, setClrBlindMode] = React.useState(false); // Enables/disables colorblind mode
    const [darkTextMode, setDarkTextMode] = React.useState(false);

    return (
        <div className="App">
            <MenuButton
                colorBlindMode={clrblindMode}
                changeColorBlindMode={setClrBlindMode}
                changeDarkTextMode={setDarkTextMode}
            />
            <HelpButton />
            <ReloadButton />
            <div className="webcam-block">
                <VideoDisplay stack={imageStack} />
                <ModeSwitcher
                    mode={trackingMode}
                    changeMode={setTrackingMode}
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
            />
            <Client
                setResponse={setResponse}
                msg={message}
                setSktState={setSocketState}
            />
            <TestComponent
                stack={imageStack}
                mode={trackingMode}
                setMsg={setMessage}
                sktState={socketState}
            />
        </div>
    );
}

export default App;
