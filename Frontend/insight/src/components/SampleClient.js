import React, { useEffect, useContext } from "react";
import { SocketContext } from "../App";
export default function SampleClient(props) {

    let socketOpen = false;
    if (props.socket) {
        props.socket.onopen = function (e) {
            console.log("[open] Connection established");
            console.log("Sending to server");
            socketOpen = true;
        };
    

        props.socket.onmessage = function (event) {
            let obj = JSON.parse(event.data);
            if (
                obj.Answer.toLowerCase() === "yes" ||
                obj.Answer.toLowerCase() === "no" ||
                obj.Answer.toLowerCase() === "neutral"
            ) {
                props.changeMessage("");
                props.setResponse(obj.Answer.toLowerCase());
            } else {
                // If the response if not a card response, it must be an error
                props.changeMessage(obj.Answer.toLowerCase());
                console.log(`[Error] Error received from server: ${props.message}`);
            }
        };

        props.socket.onclose = function (event) {
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

        props.socket.onerror = function (error) {
            console.log(`[error] ${error.message}`);
        };
    }

    // https://stackoverflow.com/questions/65049812/how-to-call-a-function-every-minute-in-a-react-component/65049865
    const SECOND_MS = 120; // Rate at which frames are sent to the server, made this lower than the VideoDisplay frame rate to prevent bottlenecks
    useEffect(() => {
        const interval = setInterval(() => {
            if (socketOpen && props.stack.length !== 0) {
                // console.log("Sending packet to server");
                // Oldest frames in the image stack array are sent first
                let item = props.stack.shift();
                let message = JSON.stringify({
                    mode: props.mode,
                    image: item,
                });
                // console.log("Sending message to server: " + message);
                props.socket.send(message);
                props.stack.length = 0;
            }
        }, SECOND_MS);

        return () => clearInterval(interval);
    });

    return <></>;
}
