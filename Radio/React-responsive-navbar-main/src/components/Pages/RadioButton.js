import ButtonSingleDown from "./../../images/buttonSingleDown.png"
import ButtonSingleUp from "./../../images/buttonSingleUp.png"

import React, { useState } from "react";

import "./RadioButton.css"

function RadioButton(props) {
    const [clicked, setClicked] = useState(true );
    const handleClicked = () =>
    {
        setClicked(!clicked);
        const checked = document.getElementById("toggleWebControl").checked;
        if (checked)
        {
            alert(clicked);

            const formData = new FormData();
            formData.append("name", props.name);
            formData.append("state", clicked);
            fetch("http://localhost:5000/button_clicked/" + props.name + "/" + clicked, {
                method: "POST",
                body: formData
            }).then();
        }
    }
    return (
        <div className="radioButton">
            
            <img src={ButtonSingleDown} alt="radio status" className="buttonOff" 
            onClick={handleClicked}/>
            { clicked ? <img src={ButtonSingleUp} alt="radio status" className="buttonOn"
            onClick={handleClicked}/>: null }
            
        </div>
    );
}

export default RadioButton;