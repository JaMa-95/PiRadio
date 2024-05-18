import React from "react";
import './Basic.css';



export const BasicRadio = () => {
    const buttonHtml = [];
    this.props.buttons.forEach(function (item, index) {
      buttonHtml.push(Button());
    });
  return (
    <div className="mainBasic">
        {buttonHtml}
    </div>
  );
};

function Button(props) {
    return (
       <label>
            name: <input type="checkbox" name="myCheckbox" />
      </label>
    );
};

