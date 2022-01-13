import React from 'react'

function WebsocketTest(props) {

    const {websocket} = props.websocket // websocket instance passed as props to this child component

    try {
        websocket.send("This is a test of the websocket connection") // send data to the server
    } catch (error) {
        console.log(error)
    }


    return (
        <div>
        </div>
    )
}

export default WebsocketTest