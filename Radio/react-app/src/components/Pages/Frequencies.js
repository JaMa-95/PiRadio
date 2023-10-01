import React from "react";
import { useState, useEffect, createRef, useRef } from 'react';
import './Frequencies.css';
import AddLogo from './images/add.svg';
import SubtractLogo from './images/subtract.svg';

export const Frequencies = (props) => {
  const frequ = ["Lang", "Mittel", "Kurz"];
  const [allFrequencies, setAllFrequencies] = useState({});
  const [frequencyList, setFrequencyList] = useState(null);
  const [currentButton, setCurrentButton] = useState(frequ[0]);
  const elementsRef = useRef([]);

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
        setFrequencyList(addIndexesToFrequencies(d));
        allFrequencies["name"] = addIndexesToFrequencies(d);
        setAllFrequencies(allFrequencies);
      })
  };

  function addIndexesToFrequencies(frequencies) {
    let frequenciesIndexes = [];
    for (let index; index <= frequencies.length; index++)
    {
        frequenciesIndexes.push({"index": index, "data": frequencies[index]});
    };
    return frequenciesIndexes;
  };

  function deleteIndexesFromFrequencies(frequenciesIndexes) {
    let frequencies = [];
    for (let index; index <= frequenciesIndexes.length; index++)
    {
      frequencies.push(frequenciesIndexes[index]["data"]);
    }
    return frequencies;
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
      .then((res) => res.json())
      .then((d) => 
      {
        // TODO: pop up success or fail check if status 200 or 404
      })
  }; 

  useEffect(() => {
    fetchFrequencyList(currentButton);
  }, []);

  const setFrequencies = (index, frequency) => {
    let frequencyListNew = [...frequencyList];
    frequencyListNew[index] = frequency;
    setFrequencyList(frequencyListNew);
  };

  const addFrequency = () => {
    let frequencyListNew = [...frequencyList];
    frequencyListNew.push({
      "index": frequencyListNew[frequencyListNew.length - 1]["index"] + 1, 
      "data": [
        {"name": "", "minimum": 0, "maximum": 1,
          "radio_name": "", "radio_url": "", "radio_url_re": ""}
      ]
    })
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

  const deleteFrequency = (index) => {
    let frequencyListNew = [...frequencyList];
    for (let i; i <= frequencyListNew.length; i++) {
      if (frequencyListNew[i]["index"] === index)
      {
        frequencyListNew.splice(i, 1);  
      }
    }
    setFrequencyList(frequencyListNew);
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
        <Buttons names={frequ} function={fetchFrequencyList} setButton={setCurrentButton}/>
      </div>
      <div>
        <img src={AddLogo} alt="Add a frequency" onClick={addFrequency}/>
      </div>
      <div>
        <button type="button" onClick={postFrequencyList}>Save Frequencies</button>
      </div>
      <div>
          {frequencyList != null &&
              frequencyList.map(function(item, index){
              return ( <div className="buttonFrequency" key={index}>
                   <Frequency name={item["name"]} radioName={item["radio_name"]} minimum={item["minimum"]} maximum={item["maximum"]}
                      url={item["radio_url"]} url_re={item["radio_url_re"]} index={index} setFrequency={setFrequencies}
                      elementsRef={elementsRef} delete={deleteFrequency}/>
                </div>);
            }
          )};
      </div>
      <div>
        <img src={AddLogo} alt="Add a frequency" onClick={addFrequency}/>
      </div>
      <div>
        <button type="button" onClick={postFrequencyList}>Save Frequencies</button>
      </div>
    </div>
  );
};

// <FrequenciesList frequencyList={frequencyList} setFrequencyList={setFrequencyList}/>

function FrequenciesList(props) {
  const getFrequencies = (index, frequency) => {
    let frequencyList = props.frequencyList;
    frequencyList[index] = frequency;
    props.setFrequencyList(frequencyList);
  };
  if (props.frequencyList == null)
  {
    return (
        <div>
          Rendering
        </div>
    );
  }
  return props.frequencyList.map((item, index) => (
    <div className="buttonFrequency" key={index}>
        <Frequency name={item["name"]} radioName={item["radioName"]} minimum={item["minimum"]} maximum={item["maximum"]}
        url={item["radio_url"]} url_re={item["radio_url_re"]} index={index} setFrequency={getFrequencies} />
    </div>
  ));
};

function Frequency(props) {
  const [name, setName] = useState(props.name);
  const [radioName, setRadioName] = useState(props.radioName);
  const [minimum, setMinimum] = useState(props.minimum);
  const [maximum, setMaximum] = useState(props.maximum);
  const [url, setUrl] = useState(props.url);
  const [urlRe, setUrlRe] = useState(props.url_re);
  const dataUpdate = () => {
    props.setFrequency(props.index, {"name": name, "minimum": minimum, "maximum": maximum,
    "radio_name": radioName, "radio_url": url, "radio_url_re": urlRe});
  };

  const updateName = (value) => {
    setName(value);
    dataUpdate();
  };
  const updateRadioName = (value) => {
    setRadioName(value);
    dataUpdate();
  };
  const updateMinimum = (value) => {
    setMinimum(value);
    dataUpdate();
  };
  const updateMaximum = (value) => {
    setMaximum(value);
    dataUpdate();
  };
  const updateUrl = (value) => {
    setUrl(value);
    dataUpdate();
  };
  const updateUrlRe = (value) => {
    setUrlRe(value);
    dataUpdate();
  };
  return (
    <div class="Frequency" key={props.index} ref={el => props.elementsRef.current[props.index] = el}>
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
        <img src={SubtractLogo} alt="Add a frequency" onClick={()=>props.delete(name, radioName)}/>        
      </div>
    </div>
  );
};

function Buttons(props) {
  return props.names.map((item, index) => (
    <div>
      <Button item={item} function={props.function} index={index}/>
    </div>
  ));
};

function Button(props) {
  return (
    <div className="buttonFrequency" key={props.index}>
        <button type="button" onClick={()=> props.function(props.item)}>{props.item}</button>
    </div>
  );
};
