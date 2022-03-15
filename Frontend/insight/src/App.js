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
import SampleClient from "./components/SampleClient";

function App() {
    // The imageStack array will contain images captured from the user's webcam
    // Images will be constantly added through the VideoDisplay component
    // Images will be sent through a websocket using the SampleClient component and the imageStack array will be cleared
    const imageStack = [];
    const [trackingMode, setTrackingMode] = React.useState("face");

    let [first_card, setFirstCard] = React.useState("card_none");
    let [second_card, setSecondCard] = React.useState("card_none");

    let [response, setResponse] = React.useState("");

    return (
        <div className="App">
            <MenuButton />
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
            />
            <SampleClient
                stack={imageStack}
                mode={trackingMode}
                response={response}
                setResponse={setResponse}
            />
        </div>
    );
}

export default App;
