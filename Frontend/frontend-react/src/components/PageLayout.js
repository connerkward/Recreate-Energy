import { Outlet } from "react-router-dom";
import Home from "../pages/Home"
import NoPage from "../pages/NoPage"
import Terminal from "../pages/Terminal"
import Nav from "../components/Nav";

// Define all imported pages here (will also be used in index.js for routes)
const PAGES = {
  "home":
  {
    url: "/",
    component: Home,
  },
  "terminal":
  {
    url: "/terminal",
    component: Terminal
  },
  "nopage": {
    url: "/*",
    component: NoPage
  }
}

// Define pages that will be in navbar here
const NAVPAGESKEYS = ["home", "terminal"]

const PageLayout = () => {
  return (
    <div>
      <Nav NAVPAGESKEYS={NAVPAGESKEYS} PAGES={PAGES}></Nav>
      <Outlet/>
      <footer style={{fontFamily:"monospace", padding:"0.25rem"}}>Recreate Energy Internal Only</footer>
    </div>
  ) 
};

// DEFINE PAGE PROPERTIES HERE
PageLayout.PAGES = PAGES

export default PageLayout;