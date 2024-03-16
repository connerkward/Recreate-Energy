import ReactWeather, { useOpenWeather } from 'react-open-weather';
import WeatherWidget from 'jb-react-weather-widget'
import { useEffect, useState } from 'react';

const Weather = () => {
  const theme = {
    color: {
      font: {
        main: 'var(--secondary-font-color)',
        timer: 'var(--secondary-font-color)',
        bottom: 'var(--secondary-font-color)',
        right: 'var(--secondary-font-color)'
      },
      icon: {
        main: 'var(--secondary-accent-color)',
        right: 'var(--secondary-accent-color)',
        bottom: 'var(--secondary-accent-color)'
      }
    },
    bg: {
      main: 'var(--bg-color)',
      right: 'rgba(0,0,0,0.1)',
      bottom: 'rgba(0,0,0,0.1)'
    },
    // spacing: {
    //   inner: '16px', // The width, height of gaps between inner elements
    //   outer: '16px' // padding of the container's element
    // },
    borderRadius: {
      container: '6px',
      element: '6px'
    }
  }

  useEffect(()=>{
    navigator.geolocation.getCurrentPosition(function(position) {
      console.log("Latitude is :", position.coords.latitude);
      console.log("Longitude is :", position.coords.longitude);
      setLoc([position.coords.latitude, position.coords.longitude])
    });
  },[])

  const [loc, setLoc] = useState(['48.137154', '11.576124'])

  const { data, isLoading, errorMessage } = useOpenWeather({
    key: 'f078d23d97b08559eacd59aa23825bec',
    lat: loc[0],
    lon: loc[1],
    lang: 'en',
    unit: 'metric', // values are (metric, standard, imperial)
  });

  return (
    <>
      {/* <ReactWeather
        isLoading={isLoading}
        errorMessage={errorMessage}
        data={data}
        lang="en"
        locationLabel="Munich"
        unitsLabels={{ temperature: 'C', windSpeed: 'Km/h' }}
        showForecast
      /> */}
      <WeatherWidget
      units="imperial"
      apiKey="576269180c6a776bab12c7568bd3b395"
      theme={theme}
      className="Weather"
      ></WeatherWidget>
    </>
  );
};

export default Weather