import React, { useState, useCallback, useEffect, useRef } from 'react';
// import Select from 'react-select'
import "./Terminal.css"
import { useAuthenticator } from '@aws-amplify/ui-react';

const COMPONENTNAME = "Terminal"

const selectOptions = [
  { value: 'chocolate', label: 'Chocolate' },
  { value: 'strawberry', label: 'Strawberry' },
  { value: 'vanilla', label: 'Vanilla' }
]

const commandTemplate = (reactorID, command, value) => {
  return {
    "reactorID": reactorID,
    "command_type": command,
    "command_value": value
  }
}

const Terminal = ({ BASEAPIURL, wsMessageHistory, setwsMessageHistory, scrollTo, wsConnectFunc}) => {
  const { user, signOut } = useAuthenticator((context) => [context.user]);

  console.log("terminal reload")
  const bottomLineRef = useRef();

  // for auto scroll
  // https://dev.to/forksofpower/autoscrolling-lists-with-react-hooks-10o7
  useEffect(() => {
    if (scrollTo){
      bottomLineRef.current.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  }, [wsMessageHistory, scrollTo])

  const [input, SetInput] = useState("");

  const handleInput = event => {
    SetInput(event.target.value)
  };

  const onKeyPress = (e) => {
    if (e.key === "Enter") {
      sendInput()
    }
  }

  const sendInput = () => {
    // if (input === "CONNECT"){
    //   wsConnectFunc()
    //   SetInput("")
    //   return
    // }
    const [reactors, command, value] = input.split(" ")
    
    const route = command === "query" ? "/api/reactor/range" : "/api/reactor/command"

    const ops = {
      method: 'POST',
      headers: new Headers({
        'Authorization': `Bearer ${user.signInUserSession.accessToken.jwtToken}`,
        "accept": "application/json",
        'Content-Type': 'application/json'
      }),
      body: JSON.stringify(commandTemplate(reactors, command, value)),
    }
    fetch(`http://${BASEAPIURL}${route}`, ops
    )
      .then((response) => {
        console.log(response)
        if (response.status !== 200) {
          throw new Error(response.status)
        }
        return response.json()
      }).catch((e) => {
        console.log(e)
        setwsMessageHistory((prev) => prev.concat({ msg: "Invalid command.", type: "alert" }));
      }).then(response_data => {
        const displayStr = command === "query" ? `${response_data.command_type} ${response_data.command_value} published to ${response_data.published_to}` : `${response_data.command_type} ${response_data.command_value} requested.`
        
        setwsMessageHistory((prev) => prev.concat({ msg: displayStr, type: "alert" }));
        console.log(displayStr);
      }).catch((e) => {
        console.log(e)
      })
    SetInput("")
  };

  const processMessage = (msg) => {
    if (msg.type === "reactor_state") {
      return JSON.stringify(msg.msg).split(',').join(', ').replace(/"/g, '');
    } else if (msg.type === "alert") {
      return JSON.stringify(msg.msg).replace(/"/g, '')
    } else {
      return JSON.stringify(msg)
    }
    // if sensor data json
    // if other json?
  }

  return (
    <div className="Terminal">
      <div className="Terminal-Hoz-Container">
        <div className="Terminal-Window">
          {wsMessageHistory ? wsMessageHistory.map((msg, i) => {
            return <div className="Terminal-Line" key={`msg-${i}`}>{`> ${processMessage(msg)}`}</div>
          }) : <li>No Messages</li>}
          <div ref={bottomLineRef} className="list-bottom"></div>
        </div>
      </div>
      <div className='Input-Container'>
        <input className='Input-Text' onChange={handleInput} placeholder="Enter command" value={input} onKeyPress={onKeyPress} />
        <button className="Input-Button" onClick={sendInput}>SEND</button>
      </div>
    </div>
  )
  

};

Terminal.displayName = COMPONENTNAME

export default Terminal;