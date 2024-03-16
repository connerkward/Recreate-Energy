import { Button } from '@aws-amplify/ui-react'
import Select from 'react-select'
import { useState, useRef, useEffect } from 'react';
import "./Export.css"
import { CSVLink, CSVDownload } from "react-csv";
import { useAuthenticator } from '@aws-amplify/ui-react';

const Export = ({ associated_reactors, ACCESSTOKEN, BASEAPIURL }) => {
  const { user, signOut } = useAuthenticator((context) => [context.user]);

  // TODO: make timestream request on button press
  // placeholder for timestream integration
  // const csvData = [
  //   ["firstname", "lastname", "email"],
  //   ["Ahmed", "Tomi", "ah@smthing.co.com"],
  //   ["Raed", "Labes", "rl@smthing.co.com"],
  //   ["Yezzi", "Min l3b", "ymin@cocococo.com"]
  // ];

  const convertdictrowstocsvformat = (dictrows) => {
    const keys = Object.keys(dictrows[0])
    var csvData = [keys];
    dictrows.map((dictrow) => {
      csvData.push(keys.map((key) => dictrow[key]))
    })
    return csvData
  }

  const [startDate, setStartDate] = useState("")
  const [endDate, setEndDate] = useState("")
  const [reactor, setReactor] = useState("")
  const showData = useRef(false)
  const [data, setData] = useState()

  const get_csv_data = (event, done) => {
    console.log(event)
    const dingo = {
      "reactorID": reactor,
      "command_type": "query",
      "command_value": { "datetime_start": startDate, "datetime_end": endDate }
    }

    console.log(startDate, endDate, reactor)
    if (startDate !== "" && endDate !== "" && reactor !== "") {
      const options = {
        method: 'POST',
        headers: new Headers({
          'Authorization': `Bearer ${user.signInUserSession.accessToken.jwtToken}`,
          "accept": "application/json",
          'Content-Type': 'application/json',
        }),
        body: JSON.stringify(dingo),
      }
      fetch(`http://${BASEAPIURL}/api/reactor/range`, options)
        .then((response) => {
          console.log(response)
          if (response.status !== 200) {
            console.log("here4")
            throw new Error(response.status)
          }
          return response.json()
        })
        .then(data => {
          console.log(data)
          const d = convertdictrowstocsvformat(data)
          console.log(d)
          showData.current = true
          setData(d)
        }).catch(() => {
          console.log("here1")
          // done(false)
        });
    } else {
      // done(false)
    }
  }

  return (
    <div className="Export">
      <h1>Export</h1>
      <div className='frow'>
        <div>
          <h3>Start Date</h3>
          <input type="date" id="start" name="start" onChange={(e) => {
            setStartDate(e.target.value)
          }} />
        </div>
        <div>
          <h3>End Date</h3>
          <input type="date" id="end" name="end" onChange={(e) => {
            setEndDate(e.target.value)

          }} />
        </div>
      </div>
      <h3>Reactor</h3>
      <div className="frow">
        <select id="reactor" name="reactor" defaultValue="Select an Option" onChange={(e) => {
          // console.log()
          setReactor(e.target.value)
          get_csv_data()
        }}>
          {associated_reactors ? associated_reactors.map(({ name, ARN }, index) => {
            return <option key={index} value={name}>{name.charAt(0).toUpperCase() + name.slice(1)}</option>
          }) : <option value={"Loading"}>Loading</option>}
          <option hidden value={"Select an Option"}>Select an Option</option>
        </select>
      </div>
      {showData.current === true ? <CSVDownload
        // onClick={get_csv_data}
        data={data}
        // asyncOnClick={true}
        filename="data.csv"
      /> : null}
      {/* <CSVLink
        onClick={get_csv_data}
        data={data.current}
        asyncOnClick={true}
        filename="data.csv"
      /> */}
      <button
        onClick={get_csv_data}
      >
        Download
      </button>
      {/* </CSVLink> */}

    </div>
  )
}

export default Export