import "./Dropdown.css";
import { useState, cloneElement } from "react";

export default function Dropdown({ trigger, menu }) {
    const [open, setOpen] = useState(false);

    const handleOpen = () => {
        setOpen(!open);
    };

    return (
        <div className="dropdown">
            {cloneElement(trigger, {
                onClick: handleOpen,
            })}
            {open ? (
                <ul className="menu">
                    {menu.map((menuItem, index) => (
                        <li key={index} className="menu-item">
                            {cloneElement(menuItem, {
                                onClick: () => {
                                    menuItem.props.onClick();
                                    setOpen(false);
                                },
                            })}
                        </li>
                    ))}
                </ul>
            ) : null}
        </div>
    );
};