import CoreCharts from "../CoreCharts"
import Score from "../Score"
import Weather from "../Weather"
import "./Charts.css"

const Charts = ({ wsMessageHistory }) => {
    return (
        <>
            <div className="ChartsContainer">
                <CoreCharts wsMessageHistory={wsMessageHistory}></CoreCharts>
                <Score></Score>                

            </div>
            <Weather></Weather>
        </>
    )
}

export default Charts
