import { BasicRadio } from "./Basic";
import { FancyRadio } from "./Fancy";
import { useState } from 'react';

export const RadioControl = () => {
  const [basicRadio, setBasicRadio] = useState([]);
  const handleSetBasicRadio = (event) => {
    setBasicRadio(event.target.checked);
  };

  const [buttons, setButtons] = useState([{"button_1": false}]);

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

  return (
    <div class="main">
        <label class="switch">
            <input type="checkbox" checked={basicRadio} onChange={handleSetBasicRadio}></input>
            <span></span>
            <p>Basic Radio</p>
            {basicRadio ? <BasicRadio buttons={buttons}/> : <FancyRadio buttons={buttons}/>}
        </label>
    </div>
  );
};
