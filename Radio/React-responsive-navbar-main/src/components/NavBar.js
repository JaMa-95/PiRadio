import React, { useState } from "react";
import { NavLink } from "react-router-dom";
import "./NavBar.css";
import "./toggleSwitch.css"

function NavBar() {
  const [click, setClick] = useState(false);
  const handleClick = () => setClick(!click);

  const [toggle, setToggle] = useState(false);
  const handleToggle = () => {
    setToggle(!toggle);
      const formData = new FormData();
      formData.append("state", toggle);
      fetch("http://localhost:5000/web_control", {
          method: "POST",
          body: formData
      }).then();
    }

  return (
    <>
      <nav className="navbar">
        <div className="nav-container">
          <NavLink exact to="/" className="nav-logo">
            PiRadio
            <i className="fas fa-code"></i>
          </NavLink>

          <ul className={click ? "nav-menu active" : "nav-menu"}>
            <li className="nav-item">
              <NavLink
                exact
                to="/"
                activeClassName="active"
                className="nav-links"
                onClick={handleClick}
              >
                Home
              </NavLink>
            </li>
            <li className="nav-item">
              <NavLink
                exact
                to="/settings"
                activeClassName="active"
                className="nav-links"
                onClick={handleClick}
              >
                Settings
              </NavLink>
            </li>
            <li className="checkboxEle">
              <label className="toggle">
                  <input id="toggleWebControl" type="checkbox" onClick={handleToggle}/>
                  <span className="slider"></span>
              </label>
              Web Control
            </li>
          </ul>
          <div className="nav-icon" onClick={handleClick}>
            <i className={click ? "fas fa-times" : "fas fa-bars"}></i>
          </div>
        </div>
      </nav>
    </>
  );
}

export default NavBar;
