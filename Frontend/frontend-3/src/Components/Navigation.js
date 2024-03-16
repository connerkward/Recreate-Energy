import recreateLogo from '../Images/logo.png'
import { NavLink, Link, Nav } from "react-router-dom";
import "./Navigation.css"
import { useAuthenticator } from '@aws-amplify/ui-react';


const Navigation = () => {
  const { user, signOut } = useAuthenticator((context) => [context.user]);
  try{
    console.log(user.signInUserSession.accessToken)
  } catch(error){
    console.log(error)
  }

  return (
    <>
      <div className="Navbar">
        <div className="NavLogoContainer">
          <NavLink className="NavLogo" to="/">
            <img src={recreateLogo} width="30" height="30" alt='...' />
            <span>Dashboard</span>
          </NavLink>
          <div className="NavLinks">
            <NavLink className="NavLink" to="/">Home</NavLink>
            <NavLink className="NavLink" to="/terminal">Terminal</NavLink>
            <NavLink className="NavLink" to="/charts">Charts</NavLink>
            <NavLink className="NavLink" to="/export">Export</NavLink>
          </div>
          <button onClick={()=>{signOut()}}>Logout</button>
        </div>
        {/* <div className="NavLinks">
          <NavLink className="NavLink" to="/">Home</NavLink>
          <NavLink className="NavLink" to="/terminal">Terminal</NavLink>
          <NavLink className="NavLink" to="/charts">Charts</NavLink>
          <NavLink className="NavLink" to="/export">Export</NavLink>
        </div> */}
      </div>
    </>
  )
}

export default Navigation
