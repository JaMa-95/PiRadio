import BasicRadio  from "./Basic";
import { FancyRadio } from "./Fancy";
import { useState, useEffect } from 'react';

export const RadioControl = (props) => {
  const [basicRadio, setBasicRadio] = useState([]);
  const handleSetBasicRadio = (event) => {
    setBasicRadio(event.target.checked);
  };

  const [buttons, setButtons] = useState([]);
  const [frequencyValues, setFrequencyValues] = useState([]);

  const fetchButtons= () => {
    return fetch('http://127.0.0.1:8000/buttons/', {
      method: 'GET',
      headers: {
          'Accept': 'application/json',
      },
  })
    .then((res) => res.json())
    .then((data) => 
    {
      setButtons(data);
    })
  };
  function handleNormalButtonChange(name, value) {
    let newButtons = [...buttons];
    newButtons.forEach((item, index) => {
        if (item.name === name) {
          newButtons[index].state = value;
        };
    });
    setButtons(newButtons);
    postButtonValue(name, value);
  };

  function handleFrequencyButtonChange(name, value) {
    let newButtons = [...buttons];
    if (!value) {
        newButtons.forEach((item, index) => {
            if (item.name === name) {
                newButtons[index].state = value;
                postButtonValue(name, value);
            };
        });
    } else {
        newButtons.forEach((item, index) => {
            if (item.name === name) {
              newButtons[index].state = value;
            } else {
              newButtons[index].state = false;
            };
            postButtonValue(name, value);
        });
    }
    setButtons(newButtons);
  };

  function postButtonValue(name, value) {
    // Send the button value to the server
    fetch('http://localhost:8000/button', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ "name": name, "value": value })
    })
    .then(response => {
        // Handle the response
    });
  }


  const fetchFrequencyValues = () => {
    return fetch('http://127.0.0.1:8000/frequency_names/', {
      method: 'GET',
      headers: {
          'Accept': 'application/json',
      },
    })
      .then((res) => res.json())
      .then((data) => {
        setFrequencyValues(data);
      });
  };

  useEffect(() => {
    fetchFrequencyValues();
    fetchButtons();
  }, []);

  return (
    <div className="main">
        <label className="switch">
            <input type="checkbox" checked={basicRadio} onChange={handleSetBasicRadio}></input>
            <span></span>
            <p>Basic Radio</p>
            {basicRadio ? <BasicRadio buttons={buttons} webControl={props.webControl} 
                            frequencyValues={frequencyValues} handleFrequencyButtons={handleFrequencyButtonChange} handleNormalButtons={handleNormalButtonChange}/> :
                          <FancyRadio buttons={buttons} webControl={props.webControl} 
                            frequencyValues={frequencyValues} handleFrequencyButtons={handleFrequencyButtonChange} handleNormalButtons={handleNormalButtonChange}/>}
        </label>
    </div>
  );
};
