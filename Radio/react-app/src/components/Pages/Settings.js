import './Settings.css';
import AddLogo from './images/add-circle.svg';
import Potentiometer from './Settings/Potentiometer';
import Button from './Settings/Button';
import General from './Settings/General';

import { useEffect, useState } from 'react';

export const Settings = (props) => {
  const [analogSettings, setAnalogSettings] = useState({});
  const [buttonsSettings, setButtonsSettings] = useState({});
  const [devices, setDevices] = useState([]);

  const fetchButtonSettings = () => {
    return fetch('http://127.0.0.1:8000/buttonsSettings/', {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
      },
    })
      .then((res) => res.json())
      .then((d) => {
        setButtonsSettings(d);
      })
  };

  useEffect(() => {
    fetchButtonSettings();
  }, []);

  const fetchAnalogSettings = () => {
    return fetch('http://127.0.0.1:8000/analogSettings/', {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
      },
    })
      .then((res) => res.json())
      .then((d) => {
        setAnalogSettings(d.sensors);
        setDevices(d.devices);
      })
  };

  const addPotentiometer = () => {
    const name = prompt("Enter the potentiometer name:");
    if (name) {
      fetch('http://127.0.0.1:8000/potentiometer', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: name
        }),
      })
        .then(response => response.json())
        .then(data => {
          // Handle the response data if needed
          console.log(data);
          window.location.reload();
        })
        .catch(error => {
          // Handle any errors
          console.error('Error:', error);
        });
    }
  };

  useEffect(() => {
    fetchButtonSettings();
    fetchAnalogSettings();
  }, []);


  return (
    <div className={props.className}>
      <div className="centerDiv">
        <h1>General</h1>
      </div>
      <General />
      <div className="centerDiv">
        <h1>Potentiometer</h1>
        <img src={AddLogo} alt="Add Potentiometer" className="add" onClick={addPotentiometer} />
      </div>
      <div className='rowA'>
        {Object.keys(analogSettings).map((analogKey) => (
          <Potentiometer
            key={analogKey}
            name={analogKey}
            settings={analogSettings[analogKey]}
            devices={devices}
          />
        ))}
      </div>
      <h1>Buttons</h1>
      <img src={AddLogo} alt="Add Button" className="add" fill="currentColor" />
      < div className='rowB'>
        {Object.keys(buttonsSettings).map((buttonKey) => (
          <Button
            key={buttonKey}
            name={buttonKey}
            settings={buttonsSettings[buttonKey]}
          />
        ))}
      </div>
    </div>
  );
};