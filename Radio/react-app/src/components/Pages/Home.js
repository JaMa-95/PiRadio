import React from "react";
import './Home.css';
import { RadioControl } from "./RadioControl/RadioControl";

export const Home = () => {
  return (
    <div class="main">
        <div class="container">
            <h1>Home</h1>
            <label class="switch">
                <input type="checkbox"></input>
                <span></span>
                <p>Web-Control</p>
            </label>
            <section>
                <RadioControl/>
            </section>
        </div>
    </div>
  );
};
