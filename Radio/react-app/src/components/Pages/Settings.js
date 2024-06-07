import './Settings.css';
import Potentiometer from './Settings/Potentiometer';
import Button from './Settings/Button';
import AddLogo from './images/add-circle.svg';

import { useEffect, useState } from 'react';

export const Settings = (props) => {
  const [buttonsSettings, setButtonsSettings] = useState({});
  const fetchButtonSettings = () => {
    return fetch('http://127.0.0.1:8000/buttonsSettings/', {
      method: 'GET',
      headers: {
          'Accept': 'application/json',
      },
  })
    .then((res) => res.json())
    .then((d) => 
    {
      console.log(JSON.stringify(d));
      setButtonsSettings(d);
    })
  };

  useEffect(() => {
    fetchButtonSettings();
  }, []);

  return (
    <div className={props.className}>
      <div className="centerDiv">
      <h1>Potentiometer</h1>
      <img src={AddLogo} alt="Add Potentiometer" className="add"/>
      </div>
      <div className='rowA'>
        <Potentiometer name="Volume"/>
        <Potentiometer name="Bass"/>
        <Potentiometer name="Treble"/>
        <Potentiometer name="Frequencies"/>
      </div>
      <h1>Buttons</h1>
      <img src={AddLogo} alt="Add Button" className="add" fill="currentColor"/>
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