import React, { useEffect } from "react";

export default function SampleClient(props) {
    let socket = new WebSocket("ws://127.0.0.1:8765/");
    let socketOpen = false;

    socket.onopen = function (e) {
        console.log("[open] Connection established");
        console.log("Sending to server");
        socketOpen = true;
    };

    socket.onmessage = function (event) {
        console.log(
            `[message] Data received from server: ${event.data.toUpperCase()}`
        );
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
    const SECOND_MS = 9; // Rate at which frames are sent to the server, made this lower than the VideoDisplay frame rate to prevent bottlenecks
    useEffect(() => {
        const interval = setInterval(() => {
            if (socketOpen && props.stack.length !== 0) {
                console.log("Sending packet to server");
                // Oldest frames in the image stack array are sent first
                let item = props.stack.shift();
                socket.send(item);
                props.stack.length = 0;
            }
        }, SECOND_MS);

        return () => clearInterval(interval);
    });

    return <div></div>;
}
