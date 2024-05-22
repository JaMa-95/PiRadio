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
    return fetch('http://127.0.0.1:8000/button_names/', {
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

  const fetchFrequencyValues = () => {
    return fetch('http://127.0.0.1:8000/frequency_names/', {
      method: 'GET',
      headers: {
          'Accept': 'application/json',
      },
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("Frequency Values:", data);
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
                            frequencyValues={frequencyValues}/> :
                          <FancyRadio buttons={buttons} webControl={props.webControl} 
                            frequencyValues={frequencyValues}/>}
        </label>
    </div>
  );
};
