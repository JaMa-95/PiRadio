import React from "react";
import { useState } from 'react';

import './Home.css';
import { RadioControl } from "./RadioControl/RadioControl";

export const Home = (props) => {
  const [webControl, setWebControl] = useState(false);
  return (
    <div class="main">
        <div class="container">
            <h1>Home</h1>
            <label class="switch">
                <input type="checkbox" checked={webControl} onChange={() => setWebControl(!webControl)}></input>
                <span></span>
                <p>Web-Control</p>
            </label>
            <section>
                <RadioControl webControl={webControl}/>
            </section>
        </div>
    </div>
  );
};
