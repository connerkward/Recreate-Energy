import CoreCharts from "../CoreCharts"
import Terminal from "../Terminal"
import "./Home.css"
import Weather from "../Weather"
import Score from "../Score"

const Home = ({ BASEAPIURL, wsMessageHistory, setwsMessageHistory, wsConnectFunc}) => {

  return (
    <div className="Home">
      <div className="ChartsContainer">
        <Score></Score>
        <CoreCharts wsMessageHistory={wsMessageHistory}></CoreCharts>
        {/* <Score></Score> */}
        {/* <Weather></Weather> */}
      </div>
      <Terminal
        wsMessageHistory={wsMessageHistory}
        setwsMessageHistory={setwsMessageHistory}
        BASEAPIURL={BASEAPIURL}
        scrollTo={true}
        wsConnectFunc={wsConnectFunc}
      ></Terminal>
    </div>
  )
}

export default Home
