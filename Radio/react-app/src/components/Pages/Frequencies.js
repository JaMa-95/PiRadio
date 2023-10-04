import React from "react";
import { useState, useEffect, useRef } from 'react';
import './Frequencies.css';
import AddLogo from './images/add.svg';
import SubtractLogo from './images/subtract.svg';

export const Frequencies = (props) => {
  const [frequencyNames, setFrequencyNames] = useState([]);
  const [allFrequencies, setAllFrequencies] = useState({});
  const [frequencyList, setFrequencyList] = useState(null);
  const [currentButton, setCurrentButton] = useState("");
  const elementsRef = useRef([]);

  const fetchFrequencyNames= () => {
      return fetch('http://127.0.0.1:8000/frequencyNames/', {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
        },
    })
      .then((res) => res.json())
      .then((d) => 
      {
        setFrequencyNames(d);
        setCurrentButton(d[0]);
        fetchFrequencyList(d[0]);
      })
  };

  const fetchFrequencyList= (name) => {
    setCurrentButton(name);
    setFrequencyList(null);
      return fetch('http://127.0.0.1:8000/frequencies/' + name, {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
        },
    })
      .then((res) => res.json())
      .then((d) => 
      {
        
        let frequenciesIndexes = addIndexesToFrequencies(d);
        setFrequencyList(frequenciesIndexes);
        allFrequencies["name"] = frequenciesIndexes;
        setAllFrequencies(allFrequencies);
      })
  };

  function addIndexesToFrequencies(frequencies) {
    if (frequencies === null) {
      return null;
    }
    for (let i = 0; i < frequencies.length; i++)
    {
      frequencies[i]["id"] = i;
    };
    return frequencies;
  };

  function deleteIndexesFromFrequencies(frequenciesIndexes) {
    for (let i; i < frequenciesIndexes.length; i++)
    {
      delete frequenciesIndexes[i].id;
    }
    return frequenciesIndexes;
  };

  const postFrequencyList = () => {
      return fetch('http://127.0.0.1:8000/frequencies/', {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify([currentButton, ...deleteIndexesFromFrequencies(frequencyList)]),
    })
      .then((response) => {
        var popup = document.getElementById("myPopup");
        if (response.status === 200)
        {
          popup.innerHTML = "success";
          popup.style.color = "green";
        } else {
          popup.innerHTML = "failed";
          popup.style.color = "red";
        }
        popup.classList.replace("hide", "show");
        setTimeout(function(){
          popup.classList.replace("show", "hide");
          }, 5000);
      })
      .then((d) => {})
  }; 

  useEffect(() => {
    fetchFrequencyNames();
    if (currentButton != "")
    {
      fetchFrequencyList(currentButton);
    }
  }, []);

  const setFrequencies = (id, frequency) => {
    let frequencyListNew = [...frequencyList];
    for (let i = 0; i < frequencyListNew.length; i++) {
      if (frequencyListNew[i].id === id) {
        frequencyListNew[i] = frequency;
        break;
      }
    }
    setFrequencyList(frequencyListNew);
  };

  const addFrequency = () => {
    let frequencyListNew = [...frequencyList];
    let index = frequencyListNew[frequencyListNew.length - 1]["index"] + 1;
    let element = {
      "index": index,
          "name": "", "minimum": 0, "maximum": 1,
          "radio_name": "", "radio_url": "", "radio_url_re": ""
    }
    frequencyListNew.push(element);
    setFrequencyList(frequencyListNew);
    waitForElm(elementsRef.current[frequencyList.length]);
    setTimeout(function(){
      const element = elementsRef.current[frequencyList.length];
      element.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'start' });
      element.style.borderColor = "red";
      element.style.borderWidth = "thick";
    }, 100);
    //window.scrollTo(0, document.body.scrollHeight + element.offsetHeight);
    setTimeout(function(){
      const element = elementsRef.current[frequencyList.length];
      element.style.borderWidth = "thin";
      element.style.borderColor = "black";
    }, 5000);
  }

  const deleteFrequency = (id) => {
    setFrequencyList(prev => prev.filter((el) => el.id !== id)); 
  }

  function waitForElm(selector) {
    return new Promise(resolve => {
        if (document.querySelector(selector)) {
            return resolve(document.querySelector(selector));
        }
        const observer = new MutationObserver(mutations => {
            if (document.querySelector(selector)) {
                observer.disconnect();
                resolve(document.querySelector(selector));
            }
        });
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    });
  }

  return (
    <div>
      <div className="buttonsFrequencies">
        <Buttons names={frequencyNames} fetchFrequencies={fetchFrequencyList} setButton={setCurrentButton}/>
      </div>
      <div className="loader">
          <img src={AddLogo} alt="Add a frequency" onClick={addFrequency} className="addLogo"/>
          <button type="button" onClick={postFrequencyList}>Save Frequencies</button>
        <div class="popup">
            <span class="popuptext" id="myPopup">Popup text...</span>
          </div>
      </div>
      <div>
          {frequencyList != null &&
              frequencyList.map((item, index) => {
              return (<div key={item["id"]}>
                   <Frequency 
                      name={item["name"]} 
                      radioName={item["radio_name"]} 
                      minimum={item["minimum"]}
                      maximum={item["maximum"]} 
                      url={item["radio_url"]} 
                      url_re={item["radio_url_re"]} 
                      id={item["id"]} 
                      setFrequency={setFrequencies}
                      elementsRef={elementsRef} 
                      delete={deleteFrequency}
                      index={index}/>
                </div>);
            }
          )};
      </div>
      <div>
        <img src={AddLogo} alt="Add a frequency" onClick={addFrequency} className="addLogo"/>
      </div>
      <div>
        <button type="button" onClick={postFrequencyList}>Save Frequencies</button>
      </div>
    </div>
  );
};

// <FrequenciesList frequencyList={frequencyList} setFrequencyList={setFrequencyList}/>
function Frequency(props) {
  const [name, setName] = useState(props.name);
  const [radioName, setRadioName] = useState(props.radioName);
  const [minimum, setMinimum] = useState(props.minimum);
  const [maximum, setMaximum] = useState(props.maximum);
  const [url, setUrl] = useState(props.url);
  const [urlRe, setUrlRe] = useState(props.url_re);
  
  const dataUpdate = (nameNew, minimumNew, maximumNew, radioNameNew, urlNew, urlReNew) => {
    props.setFrequency(props.id, {"name": nameNew, "minimum": minimumNew, "maximum": maximumNew,
    "radio_name": radioNameNew, "radio_url": urlNew, "radio_url_re": urlReNew});
  };

  const updateName = (value) => {
    setName(value);
    dataUpdate(value, minimum, maximum, radioName, url, urlRe);
  };
  const updateRadioName = (value) => {
    setRadioName(value);
    dataUpdate(name, minimum, maximum, value, url, urlRe);
  };
  const updateMinimum = (value) => {
    setMinimum(value);
    dataUpdate(name, value, maximum, radioName, url, urlRe);
  };
  const updateMaximum = (value) => {
    setMaximum(value);
    dataUpdate(name, minimum, value, radioName, url, urlRe);
  };
  const updateUrl = (value) => {
    setUrl(value);
    dataUpdate(name, minimum, maximum, radioName, value, urlRe);
  };
  const updateUrlRe = (value) => {
    setUrlRe(value);
    dataUpdate(name, minimum, maximum, radioName, url, value);
  };
  return (
    <div className="frequency" id={props.id} key={props.index} ref={el => props.elementsRef.current[props.index] = el}>
      <div className="container">
          <label for="name" className="data">Name: </label>
          <input type="text" id="name" name="name" onChange={e =>updateName(e.target.value)} value={name}/>
      </div>
      <div className="container">
          <label for="radioName" className="data">Radio station name: </label>
          <input type="text" id="radioName" name="radioName" onChange={e =>updateRadioName(e.target.value)} 
            value={radioName}/>
      </div>
      <div className="container">
          <label for="startValue" className="data">Poti start value: </label>
          <input type="text" id="startValue" name="startValue" onChange={e =>updateMinimum(e.target.value)} value={minimum}/>
      </div>
      <div className="container">
          <label for="endValue" className="data">Poti end value: </label>
          <input type="text" id="endValue" name="endValue" onChange={e =>updateMaximum(e.target.value)} value={maximum}/>
      </div>
      <div className="container">
          <label for="url" className="data">Radio URL: </label>
          <input type="text" id="url" name="url" onChange={e =>updateUrl(e.target.value)} value={url}/>
      </div>
      <div className="container">
          <label for="url_re" className="data">Radio URL Spare: </label>
          <input type="text" id="url_re" name="url_re" onChange={e =>updateUrlRe(e.target.value)} value={urlRe}/>
      </div>
      <div className="container">
        <img src={SubtractLogo} alt="Add a frequency" onClick={()=>props.delete(props.id)} className="subtractLogo"/>        
      </div>
    </div>
  );
};

function Buttons(props) {
  const [selectedButton, setSelectedButton] = useState(0);
  return props.names.map((item, index) => (
    <div className="buttons">
      <Button item={item} fetchFrequencies={props.fetchFrequencies} index={index} selected={selectedButton === index}
        buttonClicked={setSelectedButton}/>
    </div>
  ));
};

function Button(props) {
  const buttonClick = () => {
    props.fetchFrequencies(props.item);
    props.buttonClicked(props.index);
  };
  return (
    <div  key={props.index}>
        <button 
            className={props.selected ? 'buttonFrequencyActive' : 'buttonFrequencyInactive'}
            type="button" 
            onClick={buttonClick} 
            active={props.selected}>
                  {props.item}
        </button>
    </div>
  );
};
