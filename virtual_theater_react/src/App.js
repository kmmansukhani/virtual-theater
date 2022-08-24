import React, { useEffect, useState } from "react";
//import logo from "./logo.svg";
import "./App.css";
import ReactDOM from "react-dom";
import axios from "axios";

const root = ReactDOM.createRoot(document.getElementById("root"));
const MAX_PARTY_SIZE = 3;

class NameForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = { username: "" };
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({ username: event.target.value });
  }

  handleSubmit(event) {
    event.preventDefault();
    const data = JSON.stringify({
      video_id: this.props.videoId,
      username: this.state.username,
    });
    // Sending data to backend to create a new user and place them into a party
    axios
      .post("http://localhost:8000/virtual_theater/", data, {
        headers: { "Content-Type": "application/json" },
      })
      .then((response) =>
        root.render(
          <WaitingRoom
            partyId={response.data.party_id}
            userId={response.data.user_id}
            myusername={this.state.username}
            videoId={this.props.videoId}
          />
        )
      );
  }
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <p>Join a watch party</p>
          <div>
            <form onSubmit={this.handleSubmit}>
              <label>
                Name:
                <input
                  type="text"
                  value={this.state.username}
                  onChange={this.handleChange}
                />
              </label>
              <input type="submit" value="Submit" />
            </form>
          </div>
        </header>
      </div>
    );
  }
}

class WaitingRoom extends React.Component {
  constructor(props) {
    super(props);
    this.state = { usernames: [], isReadyToStart: false, chatSocket: null };
    this.leaveWatchParty = this.leaveWatchParty.bind(this);
    this.componentDidMount = this.componentDidMount.bind(this);
    this.render = this.render.bind(this);
    this.componentWillUnmount = this.componentWillUnmount.bind(this);
    this.containerEl = document.createElement("div");
    this.externalWindow = null;
  }

  componentDidMount() {
    this.externalWindow = window.open(
      "",
      "",
      "width=600,height=400,left=200,top=200"
    );
    this.externalWindow.document.body.appendChild(this.containerEl);

    const partyId = this.props.partyId;
    this.state.chatSocket = new WebSocket(
      "ws://localhost:8000/ws/waitingroom/" + partyId + "/"
    );

    this.state.chatSocket.onmessage = (e) => {
      const username = JSON.parse(e.data).username;
      const toRemove = JSON.parse(e.data).toRemove;
      if (!toRemove) {
        this.externalWindow.console.log("adding " + username);
        var newUsernames = this.state.usernames;
        newUsernames.push(username);
        this.setState({ usernames: newUsernames });
      } else {
        this.externalWindow.console.log("removing " + username);

        var newUsernames = this.state.usernames;
        var index = newUsernames.indexOf(username);
        if (index !== -1) {
          newUsernames.splice(index, 1);
          this.setState({ usernames: newUsernames });
        }
      }
    };
    this.state.chatSocket.onopen = (e) => {
      this.state.chatSocket.send(
        JSON.stringify({
          username: this.props.myusername,
          user_id: this.props.userId,
        })
      );
    };
  }

  componentWillUnmount() {
    this.externalWindow.close();
  }


  leaveWatchParty() {
    const data = JSON.stringify({
      party_id: this.props.partyId,
      user_id: this.props.userId,
    });
    this.externalWindow.console.log("leaving party");
    axios
      .post("http://localhost:8000/virtual_theater/leavewatchparty/", data, {
        headers: { "Content-Type": "application/json" },
      })
      .then((response) => {
        this.state.chatSocket.close();
        this.externalWindow.close();
        root.render(<NameForm videoId={this.props.videoId} />);
      });
  }
  arrayToString(array) {
    if (array.length === 0) {
      return "";
    }
    if (array.length === 1) {
      return array[0];
    }
    var toReturn = array[0];
    if (array.length > 1) {
      for (var i = 1; i < array.length; i++) {
        toReturn += ", " + array[i];
      }
    }
  
    return toReturn;
  }

  render() {
    var toRender = (
      <div className="App">
        <header className="App-header">
          <p>Watch Party</p>
          <div>
            <p>Current Members: </p>
            <p>{this.arrayToString(this.state.usernames)}</p>
            <p>I am {this.props.myusername}</p>
            <button onClick={this.leaveWatchParty}>Leave Watch Party</button>
          </div>
        </header>
      </div>
    );
    return ReactDOM.createPortal(toRender, this.containerEl);
  }
}

function App() {
  useEffect(() => {
    chrome.tabs.query({ currentWindow: true, active: true }, function (tabs) {
      var url;
      if (tabs.length > 0) {
        url = tabs[0].url;
      } else {
        url = "";
      }
      // If the user is on the Netflix page, then show the name form
      if (
        url.includes("www.youtube.com/watch") ||
        url.includes("www.netflix.com/watch")
      ) {
        const videoId = url.includes("www.youtube.com/watch")
          ? url.substring(url.indexOf("=") + 1, url.indexOf("&"))
          : url.split("=")[1];

        root.render(<NameForm videoId={videoId} />);

        return;
      }
    });
  }, []);
}

export default App;
