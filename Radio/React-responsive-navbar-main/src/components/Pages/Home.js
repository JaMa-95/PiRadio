import React, { useState } from "react";
import RadioFront from "./../../images/radioFront2.png"
import "./Home.css"
// import Knob from "react-simple-knob";

import Slider from "./Slider.js"
import Volume from "./Volume.js"
import RadioButton from "./RadioButton";

export const Home = () => {
    /*
  const style = {
    position: "relative",
    top: "-220px",
    left: "-400px",
    height: "200px",
    fontFamily: "Arial",
    color: "#ffffff", 
    backgroundcolor: "#dbc68b"
  };
  <Knob
  defaultPercentage={0}
  onChange={console.log}
  bg="black"
  fg="white"
  mouseSpeed={5}
  transform={p => parseInt(p * 100, 10)}
  style={style} />
  */


  return (
    <div id="radioContainer">
      <img src={RadioFront} alt="radio status" id="radio"/>
        <Slider />
        <Volume />
        <RadioButton name="on"/>
        <RadioButton name="kurz"/>
        <RadioButton name="mittel"/>
        <RadioButton name="lang"/>
        <RadioButton name="ukw"/>
        <RadioButton name="spr"/>
    </div>
  );
};
