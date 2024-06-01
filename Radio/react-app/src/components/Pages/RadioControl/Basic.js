import React from "react";
import { useState, useEffect } from 'react';
import './Basic.css';


export default function BasicRadio(props) {
    return (
        <div className="buttons">
            <section>
                <Volume webControl={props.webControl}/>
            </section>
            <section>
                <FrequencyValues webControl={props.webControl} frequencyValues={props.frequencyValues}/>
            </section>
            <section>
                <RadioFrequency webControl={props.webControl}/>
            </section>
            <section>
                <Buttons webControl={props.webControl} buttons={props.buttons} handleFrequencyButtons={props.handleFrequencyButtons} 
                handleNormalButtons={props.handleNormalButtons} />
            </section>
            <section>
                <Equalizer webControl={props.webControl}/>
            </section>
        </div>
    );
};

function Buttons(props) {
    return (
        <div>
            {props.buttons.map((button, index) => {
                if (button.type === 2) {
                    return <Button key={index} item={button} webControl={props.webControl} handle={props.handleFrequencyButtons}/>;
                } else {
                    return <Button key={index} item={button} webControl={props.webControl} handle={props.handleNormalButtons}/>;
                }
            })}
        </div>
    );
};

function Button(props) {
    return (
       <label>
            {props.item.name}: <input type="checkbox" name="myCheckbox" disabled={!props.webControl} 
                onChange={(e) => props.handle(props.item.name, e.target.checked)} checked={props.item.state}/>
      </label>
    );
};

function Volume(props) {
    const [volume, setVolume] = useState(50); // Default volume set to 50
    useEffect(() => {
        const ws = new WebSocket("ws://localhost:8000/stream/volume", 'echo-protocol');
        ws.onopen = () => {
            console.log("Connected to WebSocket volume");
        };

        ws.onmessage = function(event) {
            setVolume(JSON.parse(event.data).volume);
        };

        ws.onerror = function(event) {
            console.error("WebSocket error:", event);
        };

        ws.onclose = function(event) {
            console.log("WebSocket is closed now.");
        };
        return () => {
            ws.close();
        };
    }, []);

    const handleVolumeChange = (event) => {
        const newVolume = event.target.value;
        setVolume(newVolume);

        // Send the new volume value to the server
        fetch('http://localhost:8000/volume', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ volume: newVolume })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to update volume');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    };

    return (
        <div className="Volume">
            <label>
                Volume: <input type="range" name="volume" min="0" max="100" value={volume} 
                onChange={handleVolumeChange} disabled={!props.webControl} orient="vertical"/>
            </label>
            <p>{volume}</p>
        </div>
    );
};

function FrequencyValues(props) {
    return props.frequencyValues.map((item, index) => (
        <div>
            <FrequencyValue webControl={props.webControl} name={Object.keys(item)[0]} max={item[Object.keys(item)[0]].max} min={item[Object.keys(item)[0]].min}/>
        </div>
    ));
}

function FrequencyValue(props) {
    const [frequency, setFrequency] = useState(0);
    useEffect(() => {
        const ws = new WebSocket("ws://localhost:8000/stream/frequency_values", 'echo-protocol');

        ws.onopen = () => {
            console.log("Connected to WebSocket frequency values");
        };

        ws.onmessage = function(event) {
            const data = JSON.parse(event.data);
            setFrequency(data[props.name]);
        };

        ws.onerror = function(event) {
            console.error("WebSocket error:", event);
        };

        ws.onclose = function(event) {
            console.log("WebSocket is closed now.");
        };

        return () => {
            ws.close();
        };
    }, []);

    const handleFrequencyChange = (value) => {
        setFrequency(value);
        // Send the new frequency value to the server
        fetch('http://localhost:8000/frequency', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "name": props.name, "value": value})
        })
        .then(response => {});
    };
    return (
        <div>
            <label>
                Frequency {props.name}: <input type="range" name="frequency_value" min={props.min} max={props.max} value={frequency} 
                    onChange={(e) => handleFrequencyChange(e.target.value)} disabled={!props.webControl} />
                <p>{frequency} MHz</p>  
            </label>
        </div>
    );
};

function RadioFrequency(props) {
    const [currentRadioStation, setCurrentRadioStation] = useState('');
    const [currentSong, setCurrentSong] = useState('');
    const [radioName, setRadioName] = useState('');
    const [url, setUrl] = useState('');
    const [backupActive, setBackupActive] = useState(false);
    const [nameBackup, setNameBackup] = useState('');
    const [urlBackup, setUrlBackup] = useState('');
    const [minimum, setMinimum] = useState(0);
    const [maximum, setMaximum] = useState(0);
    const [sweetSpot, setSweetSpot] = useState(0);

    useEffect(() => {
        const ws_radio_station = new WebSocket("ws://localhost:8000/stream/current_radio", 'echo-protocol');
        const ws_radio_frequency = new WebSocket("ws://localhost:8000/stream/radio_frequency", 'echo-protocol');

        ws_radio_frequency.onopen = () => {
            console.log("Connected to WebSocket radio frequency");
        };
        ws_radio_station.onopen = () => {
            console.log("Connected to WebSocket radio station");
        };

        ws_radio_frequency.onmessage = function(event) {
            const data = JSON.parse(event.data);
            setRadioName(data.radio_name);
            setUrl(data.radio_url);
            setBackupActive(data.re_active);
            setNameBackup(data.radio_name_re);
            setUrlBackup(data.radio_url_re);
            setMinimum(data.minimum);
            setMaximum(data.maximum);
            setSweetSpot(data.sweet_spot);
            console.log("Radio frequency data:", data);
        };

        ws_radio_station.onmessage = function(event) {
            const data = JSON.parse(event.data);
            console.log("Radio station data:", data);
            setCurrentRadioStation(data.radio_station);
            setCurrentSong(data.song);
        };

        ws_radio_frequency.onerror = function(event) {
            console.error("WebSocket radio frequ error:", event);
        };
        ws_radio_station.onerror = function(event) {
            console.error("WebSocket radio station error:", event);
        };

        ws_radio_frequency.onclose = function(event) {
            console.log("WebSocket is radio frequency closed.");
        };
        ws_radio_station.onclose = function(event) {
            console.log("WebSocket is radio station closed.");
        };

        return () => {
            ws_radio_frequency.close();
        };
    }, []);

    function handleBackupActiveChange(active) {
        // Send the backup active value to the server
        fetch('http://localhost:8000/re_active', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "active": active })
        })
        .then(response => {
            // Handle the response
        });
    }

    const handleBackupActiveCheckboxChange = (isChecked) => {
        setBackupActive(isChecked);
        handleBackupActiveChange(isChecked);
    };
    
    return (
        <div>
            <label>
                Radio station: <input type="text" name="current_radio_station" value={currentRadioStation} 
                onChange={(e) => setCurrentRadioStation(e.target.value)} disabled/>
            </label>
            <label>
                Song: <input type="text" name="current_song" value={currentSong} onChange={(e) => setCurrentSong(e.target.value)} disabled/>
            </label>
            <label>
                Name: <input type="text" name="radio_name" value={radioName} onChange={(e) => setRadioName(e.target.value)} 
                disabled/>
            </label>
            <label>
                URL: <input type="text" name="url" value={url} onChange={(e) => setUrl(e.target.value)} 
                disabled/>
            </label>
            <label>
                Backup active: <input type="checkbox" name="re_active" checked={backupActive} 
                onChange={(e) => handleBackupActiveCheckboxChange(e.target.checked)} disabled={!props.webControl}/>
            </label>
            <label>
                Name Backup: <input type="text" name="name_re" value={nameBackup} onChange={(e) => setNameBackup(e.target.value)} 
                disabled/>
            </label>
            <label>
                URL Backup: <input type="text" name="url_re" value={urlBackup} onChange={(e) => setUrlBackup(e.target.value)} 
                disabled/>
            </label>
            <label>
                Minimum: <input type="number" name="min" value={minimum} onChange={(e) => setMinimum(e.target.value)} 
                disabled/>
            </label>
            <label>
                Maximum: <input type="number" name="max" value={maximum} onChange={(e) => setMaximum(e.target.value)} 
                disabled/>
            </label>
            <label>
                Sweet spot: <input type="number" name="sweet_spot" value={sweetSpot} onChange={(e) => setSweetSpot(e.target.value)} 
                disabled/>
            </label>
        </div>
    );
};

function Equalizer(props) {
    const [hz60, setHz60] = React.useState(0);
    const [hz170, setHz170] = React.useState(0);
    const [hz310, setHz310] = React.useState(0);
    const [khz1, setKhz1] = React.useState(0);
    const [khz3, setKhz3] = React.useState(0);
    const [khz6, setKhz6] = React.useState(0);
    const [khz12, setKhz12] = React.useState(0);

    useEffect(() => {
        const ws = new WebSocket("ws://localhost:8000/stream/equalizer", 'echo-protocol');

        ws.onopen = () => {
            console.log("Connected to WebSocket volume");
        };

        ws.onmessage = function(event) {
            const data = JSON.parse(event.data);
            setHz60(data.hz60);
            setHz170(data.hz170);
            setHz310(data.hz310);
            setKhz1(data.khz1);
            setKhz3(data.khz3);
            setKhz6(data.khz6);
            setKhz12(data.khz12);
        };
        ws.onerror = function(event) {
            console.error("WebSocket error:", event);
        };

        ws.onclose = function(event) {
            console.log("WebSocket is closed now.");
        };

        return () => {
            ws.close();
        };
    }, []);

    const handleEqualizerChange = () => {
        const equalizerData = {
            hz60: hz60,
            hz170: hz170,
            hz310: hz310,
            khz1: khz1,
            khz3: khz3,
            khz6: khz6,
            khz12: khz12
        };

        // Send the equalizer data to the server
        fetch('http://localhost:8000/equalizer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(equalizerData)
        })
        .then(response => {
            // Handle the response
            // ...
        });
    };

    useEffect(() => {
        // Call the handleEqualizerChange function whenever any of the equalizer values change
        handleEqualizerChange();
    }, [hz60, hz170, hz310, khz1, khz3, khz6, khz12]);

    return (
        <div className="Equalizer">
            <label>
                60 Hz: <input type="range" name="60hz" min="-20" max="20" value={hz60} onChange={(e) => {setHz60(e.target.value); handleEqualizerChange();}} 
                    disabled={!props.webControl} orient="vertical"/>
            </label>
            <label>
                170 Hz: <input type="range" name="170hz" min="-20" max="20" value={hz170} onChange={(e) => {setHz170(e.target.value); handleEqualizerChange();}}    
                    disabled={!props.webControl} orient="vertical"/>
            </label>
            <label>
                310 Hz: <input type="range" name="310hz" min="-20" max="20" value={hz310} onChange={(e) => {setHz310(e.target.value); handleEqualizerChange();}} 
                    disabled={!props.webControl} orient="vertical"/>
            </label>
            <label>
                1 kHz: <input type="range" name="1khz" min="-20" max="20" value={khz1} onChange={(e) => {setKhz1(e.target.value); handleEqualizerChange();}} 
                    disabled={!props.webControl} orient="vertical"/>
            </label>
            <label>
                3 kHz: <input type="range" name="3khz" min="-20" max="20" value={khz3} onChange={(e) => {setKhz3(e.target.value); handleEqualizerChange();}}    
                    disabled={!props.webControl} orient="vertical"/>
            </label>
            <label>
                6 kHz: <input type="range" name="6khz" min="-20" max="20" value={khz6} onChange={(e) => {setKhz6(e.target.value); handleEqualizerChange();}} 
                    disabled={!props.webControl} orient="vertical"/>
            </label>
            <label>
                12 kHz: <input type="range" name="12khz" min="-20" max="20" value={khz12} onChange={(e) => {setKhz12(e.target.value); handleEqualizerChange();}} 
                    disabled={!props.webControl} orient="vertical"/>
            </label>
        </div>
    );
};