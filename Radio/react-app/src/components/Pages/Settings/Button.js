import './Button.css'
import { useEffect, useState } from 'react';
import Dropdown from '../../../commen/Dropdown';

export default function Button(props) {
    const [name, setName] = useState(props.name);
    const [active, setActive] = useState(props.settings.active);
    const [reversed, setReversed] = useState(props.settings.reversed);
    const [pin, setPin] = useState(props.settings.pin);
    const [isOnOff, setIsOnOff] = useState(props.settings.is_on_off);
    const [isOnOffRaspi, setIsOnOffRaspi] = useState(props.settings.is_on_off_raspi);
    const [isChangeSpeaker, setIsChangeSpeaker] = useState(props.settings.is_change_speaker);
    const [freq, setFreq] = useState(props.settings.freq);
    const [action, setAction] = useState(props.settings.action);
    const [type, setType] = useState("");
    const types = ["ON/OFF Music", "ON/OFF Raspi", "Change Speaker", "Frequency"];
    const actions = {
        TURN_OFF_RASPBERRY: 0,
        STOP_MUSIC: 1,
        PLAY_MUSIC: 2,
        HOLD_FREQUENCY: 3,
        ROTATE_AUDIO_SOURCE: 4,
        SET_AUDIO_SOURCE: 5
    };
    const clickTypes = {
        BUTTON_STATE_OFF: 0,
        BUTTON_STATE_ON: 1,
        BUTTON_STATE_SHORT_CLICK: 2,
        BUTTON_STATE_LONG_CLICK: 3,
        BUTTON_STATE_DOUBLE_CLICK: 4,
        BUTTON_STATE_TO_ON: 5,
        BUTTON_STATE_TO_OFF: 6
    };

    useEffect(() => {
        if (isOnOff) {
            setType("Mute");
        } else if (isOnOffRaspi) {
            setType("ON/OFF Raspi");
        } else if (isChangeSpeaker) {
            setType("Change Speaker");
        } else {
            setType("Play Music");
        }
    }, [isOnOff, isOnOffRaspi, isChangeSpeaker, freq]);

    return (
        <div className="button">
            <input type="checkbox" name='active' id='active' checked={active} onChange={(e) => setActive(e.target.value)} />
            <h3>{props.name}</h3>
            <section>
                <div>
                    <label for="reversed" className="reversedLabel" >Reversed</label>
                    <input type="checkbox" id="reversed" name="reversed" value={reversed} onChange={(e) => setReversed(e.target.value)} />
                </div>
            </section>
            <section>
                <div>
                    <label for="pin" className="pinLabel">Pin</label>
                    <input type="number" id="pin" name="pin" value={pin} onChange={(e) => setPin(parseInt(e.target.value))} />
                </div>
            </section>
            <section>
                <label for="type" className='typeLabel'> Type: <b>{type}</b> </label>
                <div className="dropdown">
                    <Dropdown
                        trigger={<button>Click to set type</button>}
                        menu={
                            types.map((type, index) => (
                                <button key={index} onClick={() => setType(type)}>
                                    {type}
                                </button>
                            ))

                        }
                    />
                </div>
            </section>
            <section>
                <Action />
            </section>
            {type === "Play Music" && (
                <section>
                    <Frequency />
                </section>
            )}
            <div class="vertical-center">
                <button type="button" className="Delete">Delete</button>
            </div>
            <div class="vertical-center">
                <button type="button" className="Save">Save</button>
            </div>
        </div>
    );
};

function Action() {
    return (
        <div>
            <button>Add action</button>
            <div>
                <button>Add apply state</button>
                <ul>

                </ul>
                <li></li><button>Remove action</button>
            </div>
        </div>
    )
}

function ApplyState() {
    return (
        <ul>
            clickTypes.map((clickType, index) => (
            <li key={index}>{clickType}</li>
            ))
        </ul>
    )
}

function Frequency() {
    return (
        <div>
            <div>
                <label for="freqPos">Frequency position</label>
                <select id="freqPos" name="freqPos" >
                    <option value="volvo">Volvo</option>
                    <option value="saab">Saab</option>
                    <option value="mercedes">Mercedes</option>
                    <option value="audi">Audi</option>
                </select>
            </div>
            <div>
                <label for="freqMusList">Frequency music list</label>
                <select id="freqMusList" name="freqMusList" />
            </div>
        </div>
    )
}