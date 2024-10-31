import './General.css'
import { useEffect, useState } from 'react';

export default function Equalizer(props) {
    const [amplifierPin, setAmplifierPin] = useState(99);
    const [onOffButtonActivePin, setOnOffButtonActivePin] = useState(99);
    const [attinyCommPin, setAttinyCommPin] = useState(99);
    const [fmModuleAdresse, setFmModuleAdresse] = useState(99);
    const [fmActive, setFmActive] = useState(99);
    const [pinA, setPinA] = useState(99);
    const [pinB, setPinB] = useState(99);
    useEffect(() => {
        console.log("props: ", props);
    }, [props]
    );
    return (
        <div className="rowA">
            <div className='Box'>
                <label htmlFor="amplifierPin">AmplifierPin:</label>
                <input type="number"
                    id="amplifierPin" name="amplifierPin"
                    value={amplifierPin}
                    onChange={() => setAmplifierPin(!amplifierPin)} />
            </div>

            <div className='Box'>
                <h3>ON/OFF Button:</h3>
                <label htmlFor="onOffButtonActivePin">Raspberry active pin:</label>
                <input type="number"
                    id="onOffButtonActivePin"
                    value={onOffButtonActivePin}
                    onChange={() => setOnOffButtonActivePin(!onOffButtonActivePin)} />
                <label htmlFor="attinyCommPin">Attin comm pin:</label>
                <input type="number"
                    id="attinyCommPin"
                    value={attinyCommPin}
                    onChange={() => setAttinyCommPin(!attinyCommPin)} />
            </div>
            <div className='Box'>
                <h3>Audio</h3>
                <label htmlFor='audioOutputSource'>Audio Out source:</label>
                <input></input>
                <label htmlFor='fmModuleAdresse'>FM-Moduel I2C-Adresse (hex):</label>
                <input type="number"
                    id="fmModuleAdresse"
                    value={fmModuleAdresse}
                    onChange={() => setFmModuleAdresse(!fmModuleAdresse)} />
                <input type="checkbox" name='fmOn' id='fmOn' checked={fmActive} onChange={(e) => setFmActive(!fmActive)} />
            </div>
            <div className='Box'>
                <h3>Audio switch</h3>
                <label htmlFor='audioSwitcherPinA'>Pin-A:</label>
                <input type="number"
                    id="audioSwitcherPinA"
                    value={pinA}
                    onChange={() => setPinA(!pinA)} />
                <label htmlFor='audioSwitcherPinB'>Pin-B:</label>
                <input type="number"
                    id="audioSwitcherPinB"
                    value={pinB}
                    onChange={() => setPinB(!pinB)} />
                <label htmlFor='Device1'>Device 1:</label>
                <input type="number"
                    id="Device1"
                    value={pinB}
                    onChange={() => setPinB(!pinB)} />
            </div>
        </div>
    );
}