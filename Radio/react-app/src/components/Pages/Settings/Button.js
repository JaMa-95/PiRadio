import './Button.css'
import { useEffect, useState } from 'react';
import Dropdown from '../../../commen/Dropdown';
import { v4 as uuid } from 'uuid';

const clickTypes = {
    BUTTON_STATE_OFF: 0,
    BUTTON_STATE_ON: 1,
    BUTTON_STATE_SHORT_CLICK: 2,
    BUTTON_STATE_LONG_CLICK: 3,
    BUTTON_STATE_DOUBLE_CLICK: 4,
    BUTTON_STATE_TO_ON: 5,
    BUTTON_STATE_TO_OFF: 6
};

export default function Button(props) {
    const [name, setName] = useState(props.name);
    const [active, setActive] = useState(props.settings.active);
    const [reversed, setReversed] = useState(props.settings.reversed);
    const [pin, setPin] = useState(props.settings.pin);
    const [isOnOff, setIsOnOff] = useState(props.settings.is_on_off);
    const [isOnOffRaspi, setIsOnOffRaspi] = useState(props.settings.is_on_off_raspi);
    const [isChangeSpeaker, setIsChangeSpeaker] = useState(props.settings.is_change_speaker);
    const [freq, setFreq] = useState(props.settings.freq);
    const [actions, setActions] = useState(props.settings.action);
    const [type, setType] = useState("");
    const types = ["ON/OFF Music", "ON/OFF Raspi", "Change Speaker", "Frequency"];
    const actionChoices = {
        INACTIVE: 99,
        TURN_OFF_RASPBERRY: 0,
        STOP_MUSIC: 1,
        PLAY_MUSIC: 2,
        HOLD_FREQUENCY: 3,
        ROTATE_AUDIO_SOURCE: 4,
        SET_AUDIO_SOURCE: 5
    };


    // outsource functions to action class
    let handleActionChange = (key, newValue) => {
        let actionNew = actions;

        actionNew[key]["action_type"] = newValue;
        setActions(actionNew);
    }

    let handleApplyStateChange = (key, clickType, newValue) => {
        let actionNew = actions;
        if (newValue) {
            actionNew[key]["apply_state"].push(clickType);
        } else {
            actionNew[key]["apply_state"] = actionNew[key]["apply_state"].filter(state => state !== clickType);
        }
        setActions(actionNew);
    }

    let deleteAction = (key) => {
        let actionNew = actions;
        delete actionNew[key];
        setActions(actionNew);
    }

    let addAction = (key) => {

    }

    let saveButton = () => {
        let data = {
            "pin": pin,
            "reversed": reversed,
            "active": active,
            "action": actions,
            "frequency": freq,
        };

        if (isOnOff) {
            data["is_on_off"] = true;
        } else if (isOnOffRaspi) {
            data["is_on_off_raspi"] = true;
        } else if (isChangeSpeaker) {
            data["is_change_speaker"] = true;
        }

        fetch('http://127.0.0.1:8000/button', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                settings: data,
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
    }

    let deleteButton = () => {
        fetch('http://127.0.0.1:8000/button', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: name
            }),
        })
            .then(response => response.json())
            .then(data => {
                // Handle the response data if needed
                // TODO: antipattern -> delete must come from higher component
                window.location.reload();
            })
            .catch(error => {
                // Handle any errors
                console.error('Error:', error);
            });
    }

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
                {/* TODO: Open this view in extra popup */}
                <Actions name={name} clickTypes={clickTypes} actions={actions} handleActionChange={handleActionChange}
                    actionChoices={actionChoices}
                    applyStateChange={handleApplyStateChange} />
            </section>
            {type === "Play Music" && (
                <section>
                    <Frequency />
                </section>
            )}
            <div class="vertical-center">
                <button type="button" className="Delete" onClick={deleteButton}>Delete</button>
            </div>
            <div class="vertical-center">
                <button type="button" className="Save" onClick={saveButton}>Save</button>
            </div>
        </div>
    );
};

function Actions(props) {
    return (
        <div>
            <button>Add action</button>
            {
                Object.keys(props.actions).map(keyAction =>
                    <Action actionChoices={props.actionChoices} actionsKey={keyAction} handleActionChange={props.handleActionChange}
                        name={props.name} activeAction={props.actions[keyAction]["action_type"]}
                        applyStates={props.actions[keyAction]["apply_state"]}
                        applyStateChange={props.applyStateChange} />
                )
            }
        </div>
    )
}

function Action(props) {
    const uniqueKey = uuid();

    const [selectedOption, setSelectedOption] = useState(props.activeAction);
    let doActionChange = (actionKey, newValue) => {
        console.log("doActionChange: " + actionKey + " " + newValue);
        props.handleActionChange(actionKey, newValue);
        setSelectedOption(newValue)
    }


    return (
        <div class="Action">
            <h3>Action</h3>
            <div>
                {
                    Object.keys(props.actionChoices).map(key =>
                        <div>
                            <input type="radio" id={uniqueKey + props.name + key} name={props.name + uniqueKey} value={key}
                                checked={selectedOption === props.actionChoices[key]}
                                onChange={() => { doActionChange(props.actionsKey, props.actionChoices[key]) }} />
                            <label for={uniqueKey + props.name + key}>{key}</label>
                        </div>
                    )
                }
            </div>
            <ApplyState uniqueKey={uniqueKey} applyStates={props.applyStates} applyStateChange={props.applyStateChange}
                actionKey={props.actionsKey} />
            <li></li><button>Remove action</button>
        </div>
    )
}

function ApplyState(props) {
    const [applyStates, setApplyStates] = useState(props.applyStates);

    function applyStateChange(actionKey, clickType, newValue) {
        props.applyStateChange(actionKey, clickType, newValue);
        if (newValue) {
            setApplyStates([...applyStates, clickType]);
        } else {
            setApplyStates(applyStates.filter(state => state !== clickType));
        }
    }

    return (
        <ul>
            {
                Object.keys(clickTypes).map(key => (
                    <div>
                        <input type="checkbox" id={key} name={props.uniqueKey + key + "State"} value={clickTypes[key]}
                            checked={applyStates.includes(clickTypes[key])}
                            onChange={() => { applyStateChange(props.actionKey, clickTypes[key], !props.applyStates.includes(clickTypes[key])) }} />
                        <label for={key}> {key} </label><br />
                    </div>
                ))
            }
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