import './Potentiometer.css'
import { useEffect, useState, cloneElement } from 'react';

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

  useEffect(() => {
    if (isVolume) {
      setType("Volume");
    } else if (isFrequency) {
      setType("Frequency");
    } else if (isEqualizer) {
      setType("Equalizer");
    }
    setDevices(Object.keys(props.devices));
  }, [isVolume, isFrequency, isEqualizer]);

  const updatePotentiometer = () => {
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


  const mystyle = {
    float: "left",
    marginRight: "20px"
  };
  return (
    <div className="potentiometer">
      <input type="checkbox" name='on' id='on' />
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
        <label for="pin" className='pinLabel'>Pin</label>
        <input type="number" id="pin" name="pin" value={pin} onChange={(e) => setPin(parseInt(e.target.value))} />
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
        <label for="formula" className='formulaLabel'> Formula</label>
        <input type="checkbox" id="formula" name="formula" value={formula} onChange={(e) => setFormula(e.target.value)} />
      </section>
      <div class="vertical-center">
        <button type="button" className="Delete">Delete</button>
      </div>
      <div class="vertical-center">
        <button type="button" className="Save" onClick={updatePotentiometer}>Save</button>
      </div>
    </div>
  );
};

const Dropdown = ({ trigger, menu }) => {
  const [open, setOpen] = useState(false);

  const handleOpen = () => {
    setOpen(!open);
  };

  return (
    <div className="dropdown">
      {cloneElement(trigger, {
        onClick: handleOpen,
      })}
      {open ? (
        <ul className="menu">
          {menu.map((menuItem, index) => (
            <li key={index} className="menu-item">
              {cloneElement(menuItem, {
                onClick: () => {
                  menuItem.props.onClick();
                  setOpen(false);
                },
              })}
            </li>
          ))}
        </ul>
      ) : null}
    </div>
  );
};