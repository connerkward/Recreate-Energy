import { Authenticator, Button } from '@aws-amplify/ui-react'
import '@aws-amplify/ui-react/styles.css'
import { Amplify, Auth } from 'aws-amplify'
import React, { useEffect, useState, useRef } from 'react'
import { BrowserRouter, Routes, Route } from "react-router-dom";
import '../node_modules/bootstrap/dist/css/bootstrap.min.css'
import './Constants/constants.css'
import Charts from './Components/Pages/Charts';
import Home from './Components/Pages/Home'
import Export from "./Components/Pages/Export"
import Navigation from './Components/Navigation'
import Terminal from './Components/Terminal'
import NotFound from "./Components/Pages/NotFound"
import { useAuthenticator } from '@aws-amplify/ui-react';

// const BASEAPIURL = "localhost:80" // local version, does not include http
// const BASEAPIURL = "34.220.123.41:80" // AWS ECS version, does not include http
const BASEAPIURL= "lb-204399610.us-west-2.elb.amazonaws.com" // AWS ELB version, does not include http

export default function App() {
  const { user } = useAuthenticator((context) => [context.user]);
  const ws = useRef();
  const associated_reactors = useRef();
  const [wsMessageHistory, setwsMessageHistory] = useState([]); // messages recieved (after reload)

  const updateMessages = (newMsg) => {
    // Duct Tape
    // TODO: update pi to not send single qoutes (invalid json)
    // TODO: update pi to send actual data types and not just strings
    setwsMessageHistory((prev) => prev.concat([JSON.parse(newMsg.replace(/'/g, '"'))]));
  }

  const initial_calls = (atoken) => {
    console.log("initial")
    try {
      const options = {
        method: 'get',
        headers: new Headers({
          'Authorization': `Bearer ${atoken}`,
          "accept": "application/json",
        }),
      }
      fetch(`http://${BASEAPIURL}/api/reactor/active-read`, options
      )
        .then((response) => { return response.json() })
        .then(({ token, path }) => {
          if (token) {
            const url = `ws://${BASEAPIURL}${path}`
            ws.current = new WebSocket(url);
            ws.current.onopen = () => console.log("ws opened");
            ws.current.onclose = () => console.log("ws closed");
            ws.current.onmessage = (e) => { updateMessages(e.data) };
          }
        })
      fetch(`http://${BASEAPIURL}/api/user/reactors`, options
      )
        .then((response) => { console.log(response); return response.json() })
        .then((response_associated_reactors) => {
          associated_reactors.current = response_associated_reactors
        })
    } catch (error) {
      console.log("error", error);
    }
  }

  useEffect(() => {
    if (ws.current === undefined) {
      initial_calls(user.signInUserSession.accessToken.jwtToken)
    }
    return () => {
      if (ws.current !== undefined) {
        ws.current.close();
      }
    };
  }, [])

  return (
    <>
      <title>My Title</title>
      <Authenticator.Provider >
        <BrowserRouter>
          <Navigation />
          <Routes>
            <Route path="/" element={<Home
              wsMessageHistory={wsMessageHistory}
              setwsMessageHistory={setwsMessageHistory}
              BASEAPIURL={BASEAPIURL}
              wsConnectFunc={initial_calls}
            />} />
            <Route path="/terminal" element={
              <Terminal
                wsMessageHistory={wsMessageHistory}
                setwsMessageHistory={setwsMessageHistory}
                BASEAPIURL={BASEAPIURL}
                scrollTo={true}
                wsConnectFunc={initial_calls}
              />
            } />
            <Route path="/charts" element={
              <Charts
                wsMessageHistory={wsMessageHistory}
              />
            } />
            <Route path="/export" element={<Export
              associated_reactors={associated_reactors.current}
              BASEAPIURL={BASEAPIURL}
            />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </BrowserRouter>
      </Authenticator.Provider>
    </>
  )
}
