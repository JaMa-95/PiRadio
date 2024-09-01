import './Button.css'
import { useState } from 'react';


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

    console.log("Button: ", props.settings);
    console.log("active: ", active);

    const renderFreq = () => {
        if (props.freq) {
            return <Frequency />;
        }
    }
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
                {renderFreq()}
            </section>
            <div class="vertical-center">
                <button type="button" className="Delete">Delete</button>
            </div>
            <div class="vertical-center">
                <button type="button" className="Save">Save</button>
            </div>
        </div>
    );
};

function Frequency() {
    return (
        <div>
            <div>
                <label for="freqPos">Frequency position</label>
                <select id="freqPos" name="freqPos" />
            </div>
            <div>
                <label for="freqMusList">Frequency music list</label>
                <select id="freqMusList" name="freqMusList" />
            </div>
        </div>
    )
}