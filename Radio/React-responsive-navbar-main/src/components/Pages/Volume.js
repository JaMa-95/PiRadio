import "./Volume.css"
import React, { useState } from "react";

function Volume() {
    const [volume, setVolume] = useState(0);
    const handleVolume = (value) => {
        setVolume(value);
        const checked = document.getElementById("toggleWebControl").checked;
        if (checked)
        {
          const formData = new FormData();
          formData.append("state", value);
          fetch("http://localhost:5000/volume/" + value, {
              method: "POST",
              body: formData
          }).then();
        }
      }
    return (
        <input type="range" orient="vertical" id="volumeSlider"
         onChange={(event) => handleVolume(event.target.value)} value={volume} />
    );
}

export default Volume;