import './Button.css'
import {useState} from 'react';
export default function Button(props) {
    const [name, setName] = useState(props.name);
    const [active, setActive] = useState(props.settings.active);
    const [reversed, setReversed] = useState(props.settings.reversed);
    const [pin, setPin] = useState(props.settings.pin);
    const [freq, setFreq] = useState(props.settings.freq);
    const [action, setAction] = useState(props.settings.action);

    const renderFreq = () => {
        if (props.freq) {
          return <Frequency/>;
      }
    }
    return (
      <div className="button">
        <input type="checkbox" name='active' id='active'/>
        <h3>{props.name}</h3>
        <div>
            <section>
                <div>
                    <label for="reversed" className="reversedLabel">Reversed</label>
                    <input type="checkbox" id="reversed" name="reversed" />
                </div>
                <div>
                    <label for="pin" className="pinLabel">Pin</label>
                    <input type="number" id="pin" name="pin" />
                </div>
                {renderFreq()}
          </section>
        </div>
        <div class="vertical-center">
            <button type="button" className="Delete">Delete</button>
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