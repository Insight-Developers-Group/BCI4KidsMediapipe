
import React from "react"
import MenuButton from './components/MenuButton'
//import Menu from './components/Menu'
//import UploadData from './components/UploadData'
import HelpButton from './components/HelpButton'
//import HelpMenu from './components/HelpMenu'
import ReloadButton from './components/ReloadButton'
import VideoDisplay from './components/VideoDisplay'
//import ModeButton from './components/ModeButton'
import ModeSwitcher from './components/ModeSwitcher'
import CardStack from './components/CardStack'
import SampleClient from "./components/SampleClient"

function App() {

  /* code taken from https://dev.to/finallynero/using-websockets-in-react-4fkp */

  // constructor(props) {
  //       super(props);

  //       this.state = {
  //           ws: null,
  //           serverMessage: ""
  //       };
  // }

  // // single websocket instance for the own application and constantly trying to reconnect.
  // componentDidMount() {
  //   this.connect();
  // }

  // timeout = 250; // Initial timeout duration as a class variable

  // connect = () => {
  //   var ws = new WebSocket("ws://localhost:3000/ws");
  //   let that = this; // cache the this
  //   var connectInterval;

  //   // websocket onopen event listener
  //   ws.onopen = () => {
  //       console.log("connected websocket main component");

  //       this.setState({ ws: ws });

  //       that.timeout = 250; // reset timer to 250 on open of websocket connection 
  //       clearTimeout(connectInterval); // clear Interval on on open of websocket connection
  //   };

  //   ws.onmessage = evt => {
  //     const message = JSON.parse(evt.data)
  //     this.setState({dataFromServer: message})
  //     console.log(message)
  //   }

  //   // websocket onclose event listener
  //   ws.onclose = e => {
  //       console.log(
  //           `Socket is closed. Reconnect will be attempted in ${Math.min(
  //               10000 / 1000,
  //               (that.timeout + that.timeout) / 1000
  //           )} second.`,
  //           e.reason
  //       );

  //       that.timeout = that.timeout + that.timeout; //increment retry interval
  //       connectInterval = setTimeout(this.check, Math.min(10000, that.timeout)); //call check function after timeout
  //   };

  //   // websocket onerror event listener
  //   ws.onerror = err => {
  //       console.error(
  //           "Socket encountered error: ",
  //           err.message,
  //           "Closing socket"
  //       );

  //       ws.close();
  //   };
  // };

  // /**
  //    * utilited by the @function connect to check if the connection is close, if so attempts to reconnect
  //    */
  // check = () => {
  //   const { ws } = this.state;
  //   if (!ws || ws.readyState == WebSocket.CLOSED) this.connect(); //check if websocket instance is closed, if so call `connect` function.
  // };


  /* end of taken code */

  return (
    <div className="App">
      {/* <WebsocketTest websocket={this.state.ws} /> */}
      <MenuButton />
      <HelpButton />
      <ReloadButton />
      <div className="webcam-block">
        <VideoDisplay />
        <ModeSwitcher />
      </div>
      <CardStack />
      <SampleClient />
    </div>
  );

}

export default App;
