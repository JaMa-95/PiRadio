import './Settings.css';
import AddLogo from '../images/add-circle.svg';
import Potentiometer from './Potentiometer';
import Button from './Button';
import General from './General';

import { useEffect, useState } from 'react';

export const Settings = () => {
  const [analogSettings, setAnalogSettings] = useState({});
  const [buttonsSettings, setButtonsSettings] = useState({});
  const [devices, setDevices] = useState([]);

  const fetchButtonSettings = () => {
    return fetch('/api/buttonsSettings/', {
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
    return fetch('/api/analogSettings/', {
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
      fetch('/api/potentiometer', {
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
    <div className={"page"}>
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