
import { useEffect, useState } from 'react';
import { LineChart, AreaChart, Area, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Text } from 'recharts';
import { ComposedChart, RadialBarChart, RadialBar, Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Pie, PieChart, Cell } from 'recharts';
import { data, reactor_data, reactor_data_short, health_fake, radialData } from "../Constants/fakeData.js"
import "./CoreCharts.css"
import Weather from './Weather.js';

// CONSTANTS
const N_VISIBLE_POINTS = 40
const N_ROLLING_AVERAGE = 20

// TODO: move these to CSS?
const COLORS = ['var(--primary-accent-color)', 'var(--secondary-accent-color)', '#49B3FF', '#FF8042'];
const MAINCOLORS = { primary: COLORS[0], secondary: COLORS[1], tertiary: '#49B3FF' };


// For rendering datetime ticks
const dateTickFormatter = (timeStr) => {
  const options = { hour: "2-digit", minute: "2-digit", hour12: false }
  return new Date(timeStr + 'Z').toLocaleTimeString("en-US", options);
}

// For rendering Tooltip date label
const dateTooltipFormatter = (timeStr) => {
  const options = { timeZoneName: "short", }
  return new Date(timeStr + 'Z').toLocaleString("en-US", options);
}

// Some components used in every chart
const xAxisComponent = <XAxis dataKey={"datetime"} tickFormatter={dateTickFormatter} minTickGap={25} />
const yAxisComponent = <YAxis allowDecimals={true} domain={["auto", "auto"]} />
const cartesianGridComponent = <CartesianGrid strokeDasharray="3 3" />
const toolTipComponent = <Tooltip contentStyle={{ backgroundColor: "rgb(34, 34, 34, 0.98)" }} labelFormatter={dateTooltipFormatter} />

const averageLineFunc = (key) => {
  return <Line type="basisOpen" dataKey={key} stroke="#8884d8" strokeWidth={3} dot={false} />
}

// Loads slice of reactor data on first render
var reactor_data_live = reactor_data.slice(reactor_data.length - N_VISIBLE_POINTS, reactor_data.length - 1)

const CoreCharts = ({ wsMessageHistory }) => {
  console.log("core charts reload")
  const [initAnimationHasRun, setInitAnimationHasRun] = useState(false)

  // UseEffect calculates rolling average when new sensor reading appears in msg history
  // TODO: somehow display rolling average to be plotted every n points 
  useEffect(() => {
    var latestMsg = wsMessageHistory[wsMessageHistory.length - 1]
    if (latestMsg !== undefined && latestMsg.type === "reactor_state") {
      const rAvgSlice = reactor_data_live.slice(reactor_data_live.length - N_ROLLING_AVERAGE, reactor_data_live.length - 1)

      // Convert each to float and get average
      latestMsg.msg.phAvg = rAvgSlice.map((val) => {
        return parseFloat(val.ph)
      }).reduce((a, b) => {
        return a + b
      }) / rAvgSlice.length

      latestMsg.msg.doxAvg = rAvgSlice.map((val) => {
        return parseFloat(val.dox)
      }).reduce((a, b) => {
        return a + b
      }) / rAvgSlice.length

      latestMsg.msg.tempAvg = rAvgSlice.map((val) => {
        return parseFloat(val.temp)
      }).reduce((a, b) => {
        return a + b
      }) / rAvgSlice.length

      latestMsg.msg.adcrAvg = rAvgSlice.map((val) => {
        return parseFloat(val.adcr)
      }).reduce((a, b) => {
        return a + b
      }) / rAvgSlice.length

      latestMsg.msg.adcvAvg = rAvgSlice.map((val) => {
        return parseFloat(val.adcv)
      }).reduce((a, b) => {
        return a + b
      }) / rAvgSlice.length

      reactor_data_live = reactor_data_live.concat(latestMsg.msg)
      reactor_data_live.shift()

      console.log("messages updated")
      console.log(reactor_data_live)
    }
  }, [wsMessageHistory])

  return (
    <>
      {/* PH ======================================================= */}
      <div className="chart-title-container">
        <div className="chart-title">Acidity</div>
        <ResponsiveContainer className='chart-container'>
          <ComposedChart className='chart' data={reactor_data_live} margin={{ left: -25, }}>
            {xAxisComponent}
            {yAxisComponent}
            {cartesianGridComponent}
            {toolTipComponent}
            <Legend />
            <Area
              type='step'
              dataKey="ph"
              stroke={MAINCOLORS.primary}
              fillOpacity={0.4}
              fill={MAINCOLORS.primary}
              animationDuration={1500}
              isAnimationActive={!initAnimationHasRun}
              onAnimationEnd={() => { console.log("animation end"); setInitAnimationHasRun(true) }}
            />
            {averageLineFunc("phAvg")}
          </ComposedChart>
        </ResponsiveContainer>
      </div>
      {/* adcr / adcv =======================================================*/}
      <div className="chart-title-container">
        <div className="chart-title">ADC</div>
        <ResponsiveContainer className='chart-container'>
          <ComposedChart className='chart' data={reactor_data_live} margin={{ left: -25, }}>
            <defs>
              <linearGradient id="colorUv" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor={MAINCOLORS.secondary} stopOpacity={0.8} />
                <stop offset="95%" stopColor={MAINCOLORS.secondary} stopOpacity={0} />
              </linearGradient>
              <linearGradient id="colorPv" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor={MAINCOLORS.primary} stopOpacity={0.8} />
                <stop offset="95%" stopColor={MAINCOLORS.primary} stopOpacity={0} />
              </linearGradient>
            </defs>
            {cartesianGridComponent}
            {toolTipComponent}
            {xAxisComponent}
            {yAxisComponent}
            <Legend />
            <Area
              type="monotone"
              dataKey="adcv"
              stroke={MAINCOLORS.primary}
              fillOpacity={0.9}
              fill="url(#colorPv)"
              animationDuration={1500}
              isAnimationActive={!initAnimationHasRun}
            />
            <Area
              type="monotone"
              dataKey="adcr"
              stroke={MAINCOLORS.secondary}
              fillOpacity={0.9}
              fill="url(#colorUv)"
              animationDuration={1500}
              isAnimationActive={!initAnimationHasRun}
            />
          </ComposedChart>
        </ResponsiveContainer>
      </div>
      {/* DOX ======================================================= */}
      <div className="chart-title-container">
      <div className="chart-title">DoX</div>
        <ResponsiveContainer className='chart-container'>
          <ComposedChart className='chart' data={reactor_data_live} margin={{ left: -25, }}>
            {xAxisComponent}
            {yAxisComponent}
            {cartesianGridComponent}
            {toolTipComponent}
            <Legend />
            <Area
              type='monotone'
              dataKey="dox"
              stroke={MAINCOLORS.primary}
              fillOpacity={0.4}
              fill={MAINCOLORS.primary}
              animationDuration={1500}
              isAnimationActive={!initAnimationHasRun}
            />
            {averageLineFunc("doxAvg")}
          </ComposedChart>
        </ResponsiveContainer>
      </div>
      {/* TEMP ======================================================= */}
      <div className="chart-title-container">
        <div className="chart-title">Temperature</div>
        <ResponsiveContainer className='chart-container'>
          <ComposedChart className='chart' data={reactor_data_live} margin={{ left: -25, }}>
            {xAxisComponent}
            {yAxisComponent}
            {cartesianGridComponent}
            {toolTipComponent}
            <Legend />
            <Area
              type='monotone'
              dataKey="temp"
              stroke={MAINCOLORS.primary}
              fillOpacity={0.4}
              fill={MAINCOLORS.primary}
              animationDuration={1500}
              isAnimationActive={!initAnimationHasRun}
            />
            {averageLineFunc("tempAvg")}
          </ComposedChart>
        </ResponsiveContainer>
      </div>

    </>
  )
}

export default CoreCharts
