import BasicRadio from "./Basic";
import { FancyRadio } from "./Fancy";
import { useState, useEffect } from 'react';

export const RadioControl = (props) => {
  const [webControl, setWebControl] = useState(false);
  const [basicRadio, setBasicRadio] = useState([]);
  const handleSetBasicRadio = (event) => {
    setBasicRadio(event.target.checked);
  };

  const handleWebControl = (checked) => {
    setWebControl(checked);
    fetch('/api/webcontrol', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ "web_control": checked })
    })
      .then(response => {
        // Handle the response
      });
  };

  const [buttons, setButtons] = useState([]);
  const [frequencyValues, setFrequencyValues] = useState([]);

  const fetchButtons = () => {
    return fetch('/api/buttons/', {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
      },
    })
      .then((res) => res.json())
      .then((data) => {
        setButtons(data);
      })
  };

  const setupWebSocket = () => {
    const socket = new WebSocket('/socket/stream/buttons');

    socket.onopen = () => {
      console.log('WebSocket connection buttons established.');
    };

    socket.onmessage = (event) => {
      if (Object.keys(event.data).length <= 3) return;
      const data = JSON.parse(event.data);
      console.log(Object.keys(event.data).length)
      console.log("DATA:", data);
      data.forEach((item) => {
        let newButtons = [...buttons];
        newButtons.forEach((button, index) => {
          if (button.name === item.name) {
            newButtons[index].state = item.state;
          };
        });
        setButtons(newButtons);
      });
    };

    socket.onclose = () => {
      console.log('WebSocket connection button closed.');
    };

    socket.onerror = (error) => {
      console.error('WebSocket button error:', error);
    };
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
          postButtonValue(name, value);
        } else {
          if (newButtons[index].state !== false) {
            newButtons[index].state = false;
            postButtonValue(newButtons[index].name, false);
          }
        };
      });
    }
    setButtons(newButtons);
  };

  function postButtonValue(name, value) {
    console.log("POSTED: ", name, value);
    // Send the button value to the server
    fetch('/api/webControl/button', {
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
    return fetch('/api/frequency_names/', {
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
    setupWebSocket();
    fetchFrequencyValues();
    fetchButtons();
  }, []);

  return (
    <div className="main">
      <label className="switch">
        <input type="checkbox" checked={webControl} onChange={() => handleWebControl(!webControl)}></input>
        <span></span>
        <p>Web-Control</p>
      </label>
      <label className="switch">
        <input type="checkbox" checked={basicRadio} onChange={handleSetBasicRadio}></input>
        <span></span>
        <p>Basic Radio</p>
      </label>
      {basicRadio ? <BasicRadio buttons={buttons} webControl={webControl}
        frequencyValues={frequencyValues} handleFrequencyButtons={handleFrequencyButtonChange} handleNormalButtons={handleNormalButtonChange} /> :
        <FancyRadio buttons={buttons} webControl={webControl}
          frequencyValues={frequencyValues} handleFrequencyButtons={handleFrequencyButtonChange} handleNormalButtons={handleNormalButtonChange} />}
    </div>
  );
};
