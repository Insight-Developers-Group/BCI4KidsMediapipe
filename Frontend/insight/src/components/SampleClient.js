import React, { useEffect } from "react";
import CardStack from "./CardStack";

export default function SampleClient(props) {
    let socket = new WebSocket("ws://127.0.0.1:8765/");
    let socketOpen = false;
    let [resp, setResp] = React.useState("yes");
    let [err, setErr] = React.useState("e");
    socket.onopen = function (e) {
        console.log("[open] Connection established");
        console.log("Sending to server");
        socketOpen = true;
    };

    socket.onmessage = function (event) {
        let obj = JSON.parse(event.data);
        setResp(obj.Answer.toLowerCase());
        console.log(
            `[message] Data received from server: ${resp}`
        );

        // If the response if not a yes or a no, it must be an error
        if (!((obj.Answer.toLowerCase === "yes") || (obj.Answer.toLowerCase === "no"))) {
            setErr(obj.Answer.toLowerCase());
            console.log(
                `[Error] Error received from server: ${err}`
            );
        }
    };

    socket.onclose = function (event) {
        if (event.wasClean) {
            console.log(
                `[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`
            );
        } else {
            // e.g. server process killed or network down
            // event.code is usually 1006 in this case
            console.log("[close] Connection died");
        }
        socketOpen = false;
    };

    socket.onerror = function (error) {
        console.log(`[error] ${error.message}`);
    };

    // https://stackoverflow.com/questions/65049812/how-to-call-a-function-every-minute-in-a-react-component/65049865
    const SECOND_MS = 33; // Rate at which frames are sent to the server, made this lower than the VideoDisplay frame rate to prevent bottlenecks
    useEffect(() => {
        const interval = setInterval(() => {
            if (socketOpen && props.stack.length !== 0) {
                // console.log("Sending packet to server");
                // Oldest frames in the image stack array are sent first
                let item = props.stack.shift();
                socket.send(item);
                props.stack.length = 0;
            }
        }, SECOND_MS);

        return () => clearInterval(interval);
    });

    props.changeMessage(err);  // Update the message state stored in the App component
    return <div><CardStack response={resp} /></div>;
}
