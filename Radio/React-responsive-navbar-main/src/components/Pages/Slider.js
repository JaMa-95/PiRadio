import "./Slider.css"
import React, { useState } from "react";

function Slider()
{
    const [slider, setSlider] = useState(19550);
    const handleSlider = (event) => {
        setSlider(event);
        const checked = document.getElementById("toggleWebControl").checked;
        if (checked)
        {
          const formData = new FormData();
          formData.append("state", slider);
          fetch("http://localhost:5000/pos_lang_kurz_mittel/" + slider, {
              method: "POST",
              body: formData
          }).then();
        }
      }
    return (
            <input type="range" min="19550" max="21100" defaultValue="19550" className="slider"
                id="sliderRadio" onChange={(event) => handleSlider(event.target.value)} />
    );
}

export default Slider;