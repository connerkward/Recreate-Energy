import { Link } from "react-router-dom";
import Amplify, { Auth, Hub, API } from 'aws-amplify'
import React, { useState, useCallback, useEffect, useRef } from 'react';

const pageTitle = "Home"

const Home = (props) => {
  const [userText, SetUserText] = useState("")
  const [userPoolText, SetUserPoolText] = useState("")

  const checkUser = () => {
    Auth.currentAuthenticatedUser().then(user => {
      console.log('currentAuthenticatedUser', user)
      // SetUserText(user.username)
      SetUserText(`Logged in as ${user.username}`)
      SetUserPoolText(`POOL:${user.client.endpoint}`)
    }).catch(() => console.log('Not signed in'))
  }

  const login = () => {
    Auth.federatedSignIn()
  }

  const logout = () => {
    Auth.signOut().then(response => {
      console.log('logout response', response)
    }).catch(() => console.log('Error logging out.'))
  }

  const loginButtonRender = () => {
    if (props.accessToken) {
      return <button onClick={logout}>Logout</button>
    } else {
      return <button onClick={login}>Login with Hosted UI</button>
    }
  }

  return <>
    <h1>{pageTitle}</h1>
    {loginButtonRender()}
    <button onClick={checkUser}>Check User (Console)</button>
  </>;
};

Home.displayName = pageTitle
export default Home;