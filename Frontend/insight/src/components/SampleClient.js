import React, { useEffect } from 'react'

export default function SampleClient() {

    let socket = new WebSocket("ws://127.0.0.1:8765/");

    socket.onopen = function (e) {
        console.log("[open] Connection established");
        console.log("Sending to server");

    };

    socket.onmessage = function (event) {
        console.log(`[message] Data received from server: ${(event.data).toUpperCase()}`);
    };

    socket.onclose = function (event) {
        if (event.wasClean) {
            console.log(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
        } else {
            // e.g. server process killed or network down
            // event.code is usually 1006 in this case
            console.log('[close] Connection died');
        }
    };

    socket.onerror = function (error) {
        console.log(`[error] ${error.message}`);
    };

    // https://stackoverflow.com/questions/65049812/how-to-call-a-function-every-minute-in-a-react-component/65049865
    const SECOND_MS = 1000;
    useEffect(() => {
        const interval = setInterval(() => {
            console.log("Sending test packet to server");
            socket.send("This is a test packet");
        }, SECOND_MS);

        return () => clearInterval(interval);
    }, [])


    return (
        <div>
        </div>
    )
}




