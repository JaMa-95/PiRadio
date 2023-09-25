import './Settings.css';
import Potentiometer from './Settings/Potentiometer';
import Button from './Settings/Button';
import AddLogo from './images/add-circle.svg';

export const Settings = (props) => {
  return (
    <div className={props.className}>
      <div className="centerDiv">
      <h1>Potentiometer</h1>
      <img src={AddLogo} alt="Add Potentiometer" className="add"/>
      </div>
      <div className='rowA'>
        <Potentiometer name="Volume"/>
        <Potentiometer name="Bass"/>
        <Potentiometer name="Treble"/>
        <Potentiometer name="Frequencies"/>
      </div>
      <h1>Buttons</h1>
      <img src={AddLogo} alt="Add Button" className="add" fill="currentColor"/>
      <div className='rowB'>
        <Button name="Switch Raspi" freq={false}/>
        <Button name="Switch Music" freq={false}/>
        <Button name="Change Speaker" freq={false}/>
        <Button name="Language Button" freq={true}/>
        <Button name="Lang Button" freq={true}/>
        <Button name="Mittel Button" freq={true}/>
        <Button name="Kurz Button" freq={true}/>
        <Button name="UKW Button" freq={true}/>
        <Button name="TA Button" freq={true}/>
        <Button name="Jazz Button" freq={true}/>
      </div>
    </div>
  );
};