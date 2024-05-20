import React from "react";
import { useState, useEffect } from 'react';
import './Basic.css';


export default function BasicRadio(props) {
    console.log("Web Control Value:", props.webControl);
    return (
        <div className="buttons">
            <section>
                <Volume webControl={props.webControl}/>
            </section>
            <section>
                <RadioFrequency webControl={props.webControl}/>
            </section>
            <section>
                <Buttons webControl={props.webControl} buttons={props.buttons}/>
            </section>
            <section>
                <Equalizer webControl={props.webControl}/>
            </section>
        </div>
    );
};

function Buttons(props) {
    return props.buttons.map((item, index) => (
        <div>
            <Button webControl={props.webControl} name={Object.keys(item)[0]}/>
        </div>
    ));
};

function Button(props) {
    return (
       <label>
            {props.name}: <input type="checkbox" name="myCheckbox" disabled={!props.webControl}/>
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
        setVolume(event.target.value);
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

function RadioFrequency(props) {
    const [frequency, setFrequency] = useState(88); // Default frequency set to 88
    const [radioName, setRadioName] = useState('');

    const [url, setUrl] = useState('');
    const [backupActive, setBackupActive] = useState(false);
    const [nameBackup, setNameBackup] = useState('');
    const [urlBackup, setUrlBackup] = useState('');
    const [minimum, setMinimum] = useState(0);
    const [maximum, setMaximum] = useState(0);
    const [sweetSpot, setSweetSpot] = useState(0);

    useEffect(() => {
        const ws = new WebSocket("ws://localhost:8000/stream/frequency_values", 'echo-protocol');

        ws.onopen = () => {
            console.log("Connected to WebSocket frequency values");
        };

        ws.onmessage = function(event) {
            const data = JSON.parse(event.data);
            console.log("Frequency Data:", data);
            setFrequency(data.first);
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

    useEffect(() => {
        const ws = new WebSocket("ws://localhost:8000/stream/radio_frequency", 'echo-protocol');

        ws.onopen = () => {
            console.log("Connected to WebSocket volume");
        };

        ws.onmessage = function(event) {
            const data = JSON.parse(event.data);
            console.log("Frequency Data:", data);
            setFrequency(data.frequency);
            setRadioName(data.radio_name);
            setUrl(data.url);
            setBackupActive(data.re_active);
            setNameBackup(data.name_re);
            setUrlBackup(data.url_re);
            setMinimum(data.minimum);
            setMaximum(data.maximum);
            setSweetSpot(data.sweet_spot);
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

    return (
        <div>
            <label>
                <p>{frequency} MHz</p>
                Frequency: <input type="range" name="frequency_value" min="87.5" max="108" value={frequency} 
                    onChange={(e) => setFrequency(e.target.value)} disabled={!props.webControl} />
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
                onChange={(e) => setBackupActive(e.target.checked)} disabled={!props.webControl}/>
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

    return (
        <div className="Equalizer">
            <label>
                60 Hz: <input type="range" name="60hz" min="-20" max="20" value={hz60} onChange={(e) => setHz60(e.target.value)} 
                    disabled={!props.webControl} orient="vertical"/>
            </label>
            <label>
                170 Hz: <input type="range" name="170hz" min="-20" max="20" value={hz170} onChange={(e) => setHz170(e.target.value)}    
                    disabled={!props.webControl} orient="vertical"/>
            </label>
            <label>
                310 Hz: <input type="range" name="310hz" min="-20" max="20" value={hz310} onChange={(e) => setHz310(e.target.value)} 
                    disabled={!props.webControl} orient="vertical"/>
            </label>
            <label>
                1 kHz: <input type="range" name="1khz" min="-20" max="20" value={khz1} onChange={(e) => setKhz1(e.target.value)} 
                    disabled={!props.webControl} orient="vertical"/>
            </label>
            <label>
                3 kHz: <input type="range" name="3khz" min="-20" max="20" value={khz3} onChange={(e) => setKhz3(e.target.value)}    
                    disabled={!props.webControl} orient="vertical"/>
            </label>
            <label>
                6 kHz: <input type="range" name="6khz" min="-20" max="20" value={khz6} onChange={(e) => setKhz6(e.target.value)} 
                    disabled={!props.webControl} orient="vertical"/>
            </label>
            <label>
                12 kHz: <input type="range" name="12khz" min="-20" max="20" value={khz12} onChange={(e) => setKhz12(e.target.value)} 
                    disabled={!props.webControl} orient="vertical"/>
            </label>
        </div>
    );
};