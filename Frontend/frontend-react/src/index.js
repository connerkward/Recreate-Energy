import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import PageLayout from "./components/PageLayout";
import React, { useState, useCallback, useEffect } from 'react';
import useWebSocket, { ReadyState } from 'react-use-websocket';
import Amplify, { Auth, Hub, API } from 'aws-amplify'
import awsconfig from './config/awsconfig'

// React Congito Implementation
// https://www.thelambdablog.com/using-the-cognito-hosted-ui-for-authentication-with-the-amplify-client-side-library-in-react

// DEBUG: Login Info
// testuser, DingoDingo123*

// TODO: update for AWS hosting, maybe put in ENV
const baseAPIURL = "127.0.0.1:8000" // local version

// Main 
export default function App() {
  const [socketUrl, setSocketUrl] = useState(baseAPIURL); // websocket url
  const [messageHistory, setMessageHistory] = useState([]); // messages recieved (after reload)
  const [accessToken, setAccessToken] = useState(""); // messages recieved (after reload)

  // This UseEffect is called on first render, auth's with cognito, then API for websocket URL
  useEffect(() => {
    Auth.configure({ Auth: awsconfig })
    // AWS Hub listens for Cognito Events, fetches ws url from API, updates access token
    Hub.listen('auth', ({ payload: { event, data } }) => {
      switch (event) {
        case 'signIn':
        case 'cognitoHostedUI':
          console.log('Authenticated...');
          console.log(data.signInUserSession.accessToken.jwtToken);
          if (data.signInUserSession.accessToken.jwtToken) {
            fetchwsURL(data.signInUserSession.accessToken.jwtToken)
          }
          break;
        case 'signIn_failure':
        case 'cognitoHostedUI_failure':
          console.log('Error', data);
          break;
      }
    });
    // Function for fetching websocket url from API
    const fetchwsURL = (accessToken) => {
      try {
        const ops = {
          method: 'get',
          headers: new Headers({
            'Authorization': `Bearer ${accessToken}`,
            "accept": "application/json",
          }),
        }
        fetch(`http://${baseAPIURL}/api/reactor/active-read`, ops
        )
          .then((response) => { console.log(response); return response.json() })
          .then(token => {
            if (token.token) {
              console.log(token.token);
              setAccessToken(accessToken)
              return setSocketUrl(`ws://${baseAPIURL}/api/reactor/ws/${token.token}`);
              // return setSocketUrl(`ws://${baseAPIURL}/ws`);
            }
          })
      } catch (error) {
        console.log("error", error);
      }
    };
  }, []);

  // react-use-websocket package, seems to work alright, but why not use just use vanilla Websockets or SocketIO?
  // will throw error until user is logged in.
  const { sendMessage, lastMessage, readyState } = useWebSocket(socketUrl);

  // This useEffect is run when page reloads AND messages change 
  // via lastMessage and setMessageHistory
  useEffect(() => {
    if (lastMessage !== null) {
      console.log(lastMessage)
      setMessageHistory((prev) => prev.concat(lastMessage.data));
    }
  }, [lastMessage, setMessageHistory]);

  // Not really sure why this is here. Was in example for react-use-websockets
  // Frankly this syntax I have no idea about
  const wsConnectionStatus = {
    [ReadyState.CONNECTING]: 'Connecting',
    [ReadyState.OPEN]: 'Open',
    [ReadyState.CLOSING]: 'Closing',
    [ReadyState.CLOSED]: 'Closed',
    [ReadyState.UNINSTANTIATED]: 'Uninstantiated',
  }[readyState];


  // React Router wraps routes, generated from PageLayout constants. 
  // Constants should just be in a constants file instead
  // Passing props here is, interesting.
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<PageLayout />}>
          {Object.entries(PageLayout.PAGES).map(([pageKey, pageValues], i) => {
            return <Route key={`Route${i}-${pageKey}`} path={pageValues.url} element={<pageValues.component
              wsMessages={messageHistory}
              wsConnectionStatus={wsConnectionStatus}
              accessToken={accessToken}
              setMessageHistory={setMessageHistory}
              baseAPIURL={baseAPIURL} 
            />} />
          })}
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

// Boilerplate
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App/>);