import './Equalizer.css'
import { useEffect, useState } from 'react';

export default function Equalizer(props) {
    return (
        <div className="Equalizer">
            <label>
                60 Hz: <input type="range" name="60hz" min="-20" max="20" value={props.hz60} onChange={(e) => { props.setHz60(e.target.value); }}
                    disabled={!props.webControl} orient="vertical" />
            </label>
            <label>
                170 Hz: <input type="range" name="170hz" min="-20" max="20" value={props.hz170} onChange={(e) => { props.setHz170(e.target.value); }}
                    disabled={!props.webControl} orient="vertical" />
            </label>
            <label>
                310 Hz: <input type="range" name="310hz" min="-20" max="20" value={props.hz310} onChange={(e) => { props.setHz310(e.target.value); }}
                    disabled={!props.webControl} orient="vertical" />
            </label>
            <label>
                600 Hz: <input type="range" name="600hz" min="-20" max="20" value={props.hz600} onChange={(e) => { props.setHz600(e.target.value); }}
                    disabled={!props.webControl} orient="vertical" />
            </label>
            <label>
                1 kHz: <input type="range" name="1khz" min="-20" max="20" value={props.khz1} onChange={(e) => { props.setKhz1(e.target.value); }}
                    disabled={!props.webControl} orient="vertical" />
            </label>
            <label>
                3 kHz: <input type="range" name="3khz" min="-20" max="20" value={props.khz3} onChange={(e) => { props.setKhz3(e.target.value); }}
                    disabled={!props.webControl} orient="vertical" />
            </label>
            <label>
                6 kHz: <input type="range" name="6khz" min="-20" max="20" value={props.khz6} onChange={(e) => { props.setKhz6(e.target.value); }}
                    disabled={!props.webControl} orient="vertical" />
            </label>
            <label>
                12 kHz: <input type="range" name="12khz" min="-20" max="20" value={props.khz12} onChange={(e) => { props.setKhz12(e.target.value); }}
                    disabled={!props.webControl} orient="vertical" />
            </label>
        </div>
    );
};