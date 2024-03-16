import React, { useState, useCallback, useEffect, useRef } from 'react';
import Select from 'react-select'

const COMPONENTNAME = "Terminal"

// I would normally put these in its own css file 
// but were moving fast and we might toss this.
const title_style = {
  // color: "white",
  color: "#1ba836",
  backgroundColor: "black",
  padding: "10px",
  fontFamily: "Helvetica",
  borderRadius: "4px",
  margin: "0",
  marginBottom: "0.5rem"
};

const terminal_style = {
  // color: "#787878", // dark grey
  color: "#1ba836", // green
  backgroundColor: "black",
  height: "60vh",
  paddingLeft: "2.5%",
  paddingRight: "2.5%",
  paddingTop: "1.5rem",
  paddingBottom: "10px",
  height: "70vh",
  fontFamily: "consolas",
  borderRadius: "4px",
  fontFamily: "helvetica",
  // fontFamily: "monospace",
  fontSize: "1rem"
};

const terminal_window_style = {
  height: "60vh",
  // backgroundColor: "orange",
  overflow: "scroll",
  flexDirection: "column-reverse"
};

const input_container_style = {
  height: "5vh",
  display: "flex",
  flexDirection: "row",
  justifyContent: "space-between",
  marginTop: "1rem",
};

const input_style = {
  "width": "70%",
  backgroundColor: "black",
  color: "white",
  outline: "none",
  border: "none",
  fontSize: "1rem",
  // fontFamily: "monospace",
};

const button_style = {
  "width": "15%",
  color: "white",
  backgroundColor: "#d12d2d", // red
  backgroundColor: "#1ba836", // green
  backgroundColor: "black", 
  borderRadius: "4px",
  border: "1px solid #cdcdcd",
  // border: "2px solid w",
};

const terminal_line_style = {
  padding: "0.25rem",
};

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

const Terminal = ({wsMessages, accessToken,baseAPIURL, setMessageHistory}) => {
  const bottomLineRef = useRef();

  // for auto scroll
  // https://dev.to/forksofpower/autoscrolling-lists-with-react-hooks-10o7
  useEffect(() => {
    bottomLineRef.current.scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
  }, [wsMessages])

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
    const [command, value, reactors] = input.split(" ")
    console.log(command, value)
    const ops = {
      method: 'POST',
      headers: new Headers({
        'Authorization': `Bearer ${accessToken}`,
        "accept": "application/json",
        'Content-Type': 'application/json'
      }),
      body: JSON.stringify(commandTemplate(reactors, command, value)),
    }
    fetch(`http://${baseAPIURL}/api/reactor/command`, ops
    )
      .then((response) => {
        if (response.status !== 200) {
          throw new Error(response.status)
        }
        console.log(response)
        return response.json()
      }).catch((e) => {
        console.log(e)
        setMessageHistory(() => wsMessages.concat("Invalid Command."));
      }).then(response_data => {
        const displayStr = `${response_data.command_type} ${response_data.command_value} published to ${response_data.published_to}`
        setMessageHistory(() => wsMessages.concat(displayStr));
        console.log(displayStr);
      }).catch((e) => {
        console.log(e)
      })


    SetInput("")
  };

  return <>
    {/* <h1 style={title_style}>Terminal 1</h1> */}
    <div style={terminal_style}>
      <div style={terminal_window_style}>
        {wsMessages ? wsMessages.map((msg, i) => {
          return <div style={terminal_line_style} key={`msg-${i}`}>{`> ${msg}`}</div>
        }) : <li>No Messages</li>}
        <div ref={bottomLineRef} className="list-bottom"></div>
      </div>
      <div style={input_container_style}>
        <input style={input_style} onChange={handleInput} placeholder="Enter command" value={input} onKeyPress={onKeyPress} />
        <button style={button_style} onClick={sendInput}>SEND</button>
      </div>
      {/* <div>
        <Select isMulti options={selectOptions} />
        <Select isMulti options={selectOptions} />
        <Select isMulti options={selectOptions} />
      </div> */}
    </div>
  </>
};

Terminal.displayName = COMPONENTNAME

export default Terminal;