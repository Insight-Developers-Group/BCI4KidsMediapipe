import React, { useEffect } from "react";

export default function TestComponent(props) {
    // https://stackoverflow.com/questions/65049812/how-to-call-a-function-every-minute-in-a-react-component/65049865
    const SECOND_MS = 120; // Rate at which frames are sent to the server, made this lower than the VideoDisplay frame rate to prevent bottlenecks
    useEffect(() => {
        const interval = setInterval(() => {
            if (props.socketState && props.stack.length !== 0) {
                // console.log("Sending packet to server");
                // Oldest frames in the image stack array are sent first
                let item = props.stack.shift();
                let message = JSON.stringify({
                    mode: props.mode,
                    image: item,
                });
                // console.log("Sending message to server: " + message);
                // socket.send(message);
                props.setMsg(message);
                props.stack.length = 0;
            }
        }, SECOND_MS);

        return () => clearInterval(interval);
    });

    return <div></div>;
}
