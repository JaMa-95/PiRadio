import './Potentiometer.css'
import { useEffect, useState, cloneElement } from 'react';
import Equalizer from './Equalizer';
import Dropdown from '../../../commen/Dropdown';

export default function Potentiometer(props) {
  const [min, setMin] = useState(props.settings.min);
  const [max, setMax] = useState(props.settings.max);
  const [formula, setFormula] = useState(props.formula);
  const [on, setOn] = useState(props.settings.on);
  const [isVolume, steIsVolume] = useState(props.settings.is_volume);
  const [isFrequency, setIsFrequency] = useState(props.settings.is_frequency);
  const [isEqualizer, setIsEqualizer] = useState(props.settings.is_equalizer);
  const [pin, setPin] = useState(props.settings.pin);
  const [device, setDevice] = useState(props.settings.device);
  const [type, setType] = useState("");
  const [devices, setDevices] = useState([]);

  const [hz60, setHz60] = useState(0);
  const [hz170, setHz170] = useState(0);
  const [hz310, setHz310] = useState(0);
  const [hz600, setHz600] = useState(0);
  const [khz1, setKhz1] = useState(0);
  const [khz3, setKhz3] = useState(0);
  const [khz6, setKhz6] = useState(0);
  const [khz12, setKhz12] = useState(0);

  useEffect(() => {
    if (isVolume) {
      setType("Volume");
    } else if (isFrequency) {
      setType("Frequency");
    } else if (isEqualizer) {
      setType("Equalizer");
      setEqualizer();
    }
    setDevices(Object.keys(props.devices));
  }, [isVolume, isFrequency, isEqualizer]);

  const setEqualizer = () => {
    setHz60(props.settings["equalizer_reduction"]["60Hz"]);
    setHz170(props.settings["equalizer_reduction"]["170Hz"]);
    setHz310(props.settings["equalizer_reduction"]["310Hz"]);
    setHz600(props.settings["equalizer_reduction"]["600Hz"]);
    setKhz1(props.settings["equalizer_reduction"]["1kHz"]);
    setKhz3(props.settings["equalizer_reduction"]["3kHz"]);
    setKhz6(props.settings["equalizer_reduction"]["6kHz"]);
    setKhz12(props.settings["equalizer_reduction"]["12kHz"]);
  };

  const getPotiData = () => {
    const potentiometerData = {
      min: min,
      max: max,
      formula: formula,
      on: on,
      is_volume: isVolume,
      is_frequency: isFrequency,
      is_equalizer: isEqualizer,
      pin: pin,
      device: device,
    };
    if (isEqualizer) {
      potentiometerData.equalizer_reduction = {
        hz60: hz60,
        hz170: hz170,
        hz310: hz310,
        hz600: hz600,
        khz1: khz1,
        khz3: khz3,
        khz6: khz6,
        khz12: khz12
      };
    }
    return potentiometerData;
  };

  const updatePotentiometer = () => {
    const potentiometerData = getPotiData();
    console.log(potentiometerData);

    let name = props.name;

    fetch('http://127.0.0.1:8000/potentiometer', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        settings: potentiometerData,
        name: name
      }),
    })
      .then(response => response.json())
      .then(data => {
        // Handle the response data if needed
        console.log(data);
      })
      .catch(error => {
        // Handle any errors
        console.error('Error:', error);
      });
  };

  const deletePotentiometer = () => {
    fetch('http://127.0.0.1:8000/potentiometer', {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name: props.name
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
  };


  const setTypeVolume = () => {
    steIsVolume(true);
    setIsEqualizer(false);
    setIsFrequency(false);
    setType("Volume");
  };

  const setTypeFrequency = () => {
    setIsFrequency(true);
    steIsVolume(false);
    setIsEqualizer(false);
    setType("Frequency");
  };

  const setTypeEqualizer = () => {
    setIsEqualizer(true);
    steIsVolume(false);
    setIsFrequency(false);
    setType("Equalizer");
  };

  const openEqualizer = () => {
    let equalizer = document.getElementById("Equalizer" + props.name);
    let equalizerButton = document.getElementById("openEqualizerButton" + props.name);
    if (equalizer.style.display === "none") {
      equalizerButton.innerHTML = "Close equalizer";
      equalizer.style.display = "block";
    } else {
      equalizerButton.innerHTML = "Open equalizer";
      equalizer.style.display = "none";
    }
  };

  const mystyle = {
    float: "left",
    marginRight: "20px"
  };

  return (
    <div className="potentiometer">
      <input type="checkbox" name='on' id='on' checked={on} onChange={(e) => setOn(e.target.value)} />
      <h3>{props.name}</h3>
      <section>
        <div style={mystyle}>
          <label for="minimum">Minimum</label>
          <input type="number" id="minimum" name="minimum" value={min} onChange={(e) => setMin(parseInt(e.target.value))} />
        </div>
      </section>
      <section>
        <div style={{ float: "left" }}>
          <label for="maximum">Maximum</label>
          <input type="number" id="maximum" name="maximum" value={max} onChange={(e) => setMax(parseInt(e.target.value))} />
        </div>
        <br style={{ clear: "both" }} />
      </section>
      <section>
        <label for="type" className='typeLabel'> Type: <b>{type}</b> </label>
        <div className="dropdown">
          <Dropdown
            trigger={<button>Click to set poti type</button>}
            menu={[
              <button onClick={setTypeVolume}> Volume </button>,
              <button onClick={setTypeFrequency}> Frequency </button>,
              <button onClick={setTypeEqualizer}> Equalizer </button>
            ]}
          />
        </div>
      </section>
      <section>
        <label for="type" className='typeLabel'> Device: <b>{device}</b> </label>
        <div className="dropdown">
          <Dropdown
            trigger={<button>Click to set device</button>}
            menu={
              devices.map((device, index) => (
                <button key={index} onClick={() => setDevice(device)}>
                  {device}
                </button>
              ))

            }
          />
        </div>
      </section>
      <section>
        <label for="pin" className='pinLabel'>Pin</label>
        <input type="number" id="pin" name="pin" value={pin} onChange={(e) => setPin(parseInt(e.target.value))} />
      </section>
      <section>
        <label for="formula" className='formulaLabel'> Formula</label>
        <input type="checkbox" id="formula" name="formula" value={formula} onChange={(e) => setFormula(e.target.value)} />
      </section>
      {isEqualizer && (
        <section>
          <button id={"openEqualizerButton" + props.name} type="button" className="Add" onClick={openEqualizer}>Open equalizer</button>
          <div style={{ display: "none" }} id={"Equalizer" + props.name}>
            <Equalizer
              hz60={hz60}
              hz170={hz170}
              hz310={hz310}
              hz600={hz600}
              khz1={khz1}
              khz3={khz3}
              khz6={khz6}
              khz12={khz12}
              setHz60={setHz60}
              setHz170={setHz170}
              setHz310={setHz310}
              setHz600={setHz600}
              setKhz1={setKhz1}
              setKhz3={setKhz3}
              setKhz6={setKhz6}
              setKhz12={setKhz12}
            />
          </div>
        </section>
      )}
      <div class="vertical-center">
        <button type="button" className="Delete" onClick={deletePotentiometer}>Delete</button>
      </div>
      <div class="vertical-center">
        <button type="button" className="Save" onClick={updatePotentiometer}>Save</button>
      </div>
    </div>
  );
};