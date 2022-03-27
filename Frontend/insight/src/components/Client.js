import React, { useEffect } from "react";

export default function SampleClient(props) {
    let socket = new WebSocket("ws://127.0.0.1:8765/");
    //let socketOpen = false;
    socket.onopen = function (e) {
        console.log("[open] Connection established");
        console.log("Sending to server");
        // socketOpen = true;
        props.setSktState(true);
    };

    socket.onmessage = function (event) {
        let obj = JSON.parse(event.data);
        props.setResponse(obj.Answer.toLowerCase());
        //console.log(`[message] Data received from server: ${props.response}`);
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
        // socketOpen = false;
        props.setSktState(false);
    };

    socket.onerror = function (error) {
        console.log(`[error] ${error.message}`);
    };

    useEffect(() => {
        socket.send(props.msg);
    }, [props.msg])

    return <div></div>;
}
