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
  const [frequenciesTestRunning, setFrequenciesTestRunning] = useState(false);
  const [stopTest, setStopTest] = useState(false);
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
    // setFrequenciesTestRunning(false);
    fetchFrequencyNames();
    setCurrentButton(frequencyNames[0]);
    if (currentButton != "")
    {
      fetchFrequencyList(currentButton);
    }
  }, []);

  const setFrequency = (id, frequency) => {
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
      "radio_name": "", "radio_name_re": "", 
      "radio_url": "", "radio_url_re": "",
      "re_active": false
    };
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
  };

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
  };

  function sleep(milliseconds) {
    var start = new Date().getTime();
    for (var i = 0; i < 1e7; i++) {
      if ((new Date().getTime() - start) > milliseconds){
        break;
      }
    }
  }

  const startTestFrequencyList = () => {
    if (frequenciesTestRunning) {
      window.alert("STOP TEST")
      setStopTest(true);
    } else {
      setFrequenciesTestRunning(true);
      testFrequencyList();
    }
  }

  const testFrequencyList = async () => { 
    let index = 0;
    for (const item of frequencyList) {
      try {
        // Stop the fetching
        window.alert("Stop test: " + stopTest)
        if (stopTest) {
          window.alert("BREAK: " + frequenciesTestRunning + " " + index);
          setFrequency(item.id, {"name": item.name, "minimum": item.minimum, "maximum": item.maximum,
          "radio_name": item.radio_name, "radio_name_re": item.radio_name_re, "radio_url": item.radio_url, 
          "radio_url_re": item.radio_url_re, "re_active": item.re_active, "url_state": item.url_state,
          "url_state_re": item.url_state_re, "attention": false});
          stopTest(false);
          setFrequenciesTestRunning(false);
          return;
        }
        index++;
        
        item.attention = true; // Set attention to true before fetching
        // Update the state to trigger re-render
        setFrequency(item.id, {"name": item.name, "minimum": item.minimum, "maximum": item.maximum,
          "radio_name": item.radio_name, "radio_name_re": item.radio_name_re, "radio_url": item.radio_url, 
          "radio_url_re": item.radio_url_re, "re_active": item.re_active, "url_state": item.url_state,
          "url_state_re": item.url_state_re, "attention": item.attention});
        
        const response = await fetch('http://127.0.0.1:8000/frequency/testWithRe/', {
          method: 'POST',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({"url": item.radio_url, "url_re": item.radio_url_re}),
        });
        const testResult = await response.json();
        // window.alert(JSON.stringify(testResult))
        if (testResult[0]) {
          item.url_state = "green";
          item.re_active = false;
        } else if (testResult[0] == false) {
          item.url_state = "red";
          item.re_active = true;
        } else {
          item.url_state = "black";
        }

        if (testResult[1] == true) {
          item.url_state_re = "green";
        } else if (testResult[1] == false) {
          item.url_state_re = "red";
        } else {
          item.url_state_re = "black";
        }

        if (testResult[0] === false && !item.url_re) {
          item.re_active = false;
        } 

        item.attention = false; // Set attention to false after fetching
        setFrequency(item.id, {"name": item.name, "minimum": item.minimum, "maximum": item.maximum,
          "radio_name": item.radio_name, "radio_name_re": item.radio_name_re, "radio_url": item.radio_url, 
          "radio_url_re": item.radio_url_re, "re_active": item.re_active, "url_state": item.url_state,
          "url_state_re": item.url_state_re, "attention": item.attention});// Update the state to trigger re-render
      } catch (error) {
        console.error('Error:', error);
      }
    }
    window.alert("FINISHED")
    setFrequenciesTestRunning(false);
    if (index >= frequencyList.length) {index--};
    setFrequency(frequencyList[index].id, 
      {"name": frequencyList[index].name, 
        "minimum": frequencyList[index].minimum, 
        "maximum": frequencyList[index].maximum,
        "radio_name": frequencyList[index].radio_name, 
        "radio_name_re": frequencyList[index].radio_name_re, 
        "radio_url": frequencyList[index].radio_url, 
        "radio_url_re": frequencyList[index].radio_url_re, 
        "re_active": frequencyList[index].re_active, 
        "url_state": frequencyList[index].url_state,
        "url_state_re": frequencyList[index].url_state_re, 
        "attention": false});
  }

  return (
    <div>
      <div className="buttonsFrequencies">
        <Buttons names={frequencyNames} fetchFrequencies={fetchFrequencyList} setButton={setCurrentButton} 
          testRunning={frequenciesTestRunning} setStopTest={setStopTest}/>
      </div>
      <div className="loader">
          <img src={AddLogo} alt="Add a frequency" onClick={addFrequency} className="addLogo"/>
          <button type="button" onClick={postFrequencyList}>Save Frequencies</button>
          <div className="popup">
            <span className="popuptext" id="myPopup">Popup text...</span>
          </div>
          <button type="button" onClick={startTestFrequencyList}>{frequenciesTestRunning ? 'Stop Test Frequency' : 'Start Test Frequency'}</button>
      </div>
      <div>
          {frequencyList != null &&
              frequencyList.map((item, index) => {
              return (<div key={item["id"]}>
                   <Frequency 
                      name={item["name"]} 
                      radioName={item["radio_name"]} 
                      radioNameRe={item["radio_name_re"]} 
                      minimum={item["minimum"]}
                      maximum={item["maximum"]} 
                      url={item["radio_url"]} 
                      url_re={item["radio_url_re"]} 
                      re_active={item["re_active"]}
                      url_state={item["url_state"]} 
                      url_state_re={item["url_state_re"]}
                      attention={item["attention"]}
                      id={item["id"]} 
                      setFrequency={setFrequency}
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
  const [radioNameRe, setRadioNameRe] = useState(props.radioNameRe);
  const [minimum, setMinimum] = useState(props.minimum);
  const [maximum, setMaximum] = useState(props.maximum);
  const [url, setUrl] = useState(props.url);
  const [urlRe, setUrlRe] = useState(props.url_re);
  const [reActive, setReActive] = useState(props.re_active);
  const [urlState, setUrlState] = useState(props.url_state);
  const [urlStateRe, setUrlStateRe] = useState(props.url_state_re);
  const [attention, setAttention] = useState(props.attention);

  const testURL = async () => {
    setAttention(true);
    try {
      const response = await fetch('http://127.0.0.1:8000/frequency/testWithRe/', {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'charset':'utf-8'
        },
        body: JSON.stringify({"url": url, "url_re": urlRe}),
      });
      const testResult = await response.json();
      // window.alert(JSON.stringify(testResult))
      if (testResult[0]) {
        setReActive(false);
        setUrlState("green");
      } else if (testResult[0] === false) {
        setReActive(true);
        setUrlState("red");
      } else {
        setUrlState("black");
      }

      if (testResult[1] === true) {
        setUrlStateRe("green");
      } else if (testResult[1] === false) {
        setUrlStateRe("red");
      } else {
        setUrlStateRe("black");
      }
      if (testResult[0] === false && !urlRe) {
        setReActive(false);
      } 
      setAttention(false);
    } catch (error) {
      window.alert("ERROR")
      console.error(error);
    }
  };
  
  const dataUpdate = (nameNew, minimumNew, maximumNew, radioNameNew, radioNameReNew, urlNew, 
                        urlReNew, reActiveNew, urlStateNew, urlStateReNew) => {
    props.setFrequency(props.id, {"name": nameNew, "minimum": minimumNew, "maximum": maximumNew,
    "radio_name": radioNameNew, "radio_name_re": radioNameReNew, "radio_url": urlNew, 
    "radio_url_re": urlReNew, "re_active": reActiveNew, "url_state": urlStateNew,
    "url_state_re": urlStateReNew, "attention": attention});
  };

  const updateAll = () => {
    dataUpdate(name, minimum, maximum, radioName, radioNameRe, url, urlRe, reActive, urlState, urlStateRe);
  };

  const updateName = (value) => {
    setName(value);
    dataUpdate(value, minimum, maximum, radioName, radioNameRe, url, urlRe, reActive, urlState, urlStateRe);
  };
  const updateRadioName = (value) => {
    setRadioName(value);
    dataUpdate(name, minimum, maximum, value, radioNameRe, url, urlRe, reActive, urlState, urlStateRe);
  };
  const updateRadioNameRe = (value) => {
    setRadioNameRe(value);
    dataUpdate(name, minimum, maximum, radioName, value, url, urlRe, reActive, urlState, urlStateRe);
  };
  const updateMinimum = (value) => {
    setMinimum(value);
    dataUpdate(name, value, maximum, radioName, radioNameRe, url, urlRe, reActive, urlState, urlStateRe);
  };
  const updateMaximum = (value) => {
    setMaximum(value);
    dataUpdate(name, minimum, value, radioName, radioNameRe, url, urlRe, reActive, urlState, urlStateRe);
  };
  const updateUrl = (value) => {
    setUrl(value);
    dataUpdate(name, minimum, maximum, radioName, radioNameRe, url, urlRe, reActive, urlState, urlStateRe);
  };
  const updateUrlRe = (value) => {
    setUrlRe(value);
    dataUpdate(name, minimum, maximum, radioName, radioNameRe, url, value, reActive, urlState, urlStateRe);
  };
  const updateReActive = (value) => {
    setReActive(value);
    dataUpdate(name, minimum, maximum, radioName, radioNameRe, url, urlRe, value, urlState, urlStateRe);
  };
  
  const updateUrlState = (value) => {
    setUrlState(value);
    dataUpdate(name, minimum, maximum, radioName, radioNameRe, url, urlRe, reActive, value, urlStateRe);
  };
  
  const updateUrlStateRe = (value) => {
    setUrlStateRe(value);
    dataUpdate(name, minimum, maximum, radioName, radioNameRe, url, urlRe, reActive, urlState, value);
  };
  
  
  return (
    <div className={attention ? "frequency attention" : "frequency"} id={props.id} key={props.index} ref={el => props.elementsRef.current[props.index] = el}>
      <div className="container">
          <label htmlFor="name" className="data">Name: </label>
          <input type="text" id="name" name="name" onChange={e =>updateName(e.target.value)} value={name}/>
      </div>
      <div className="container">
          <label htmlFor="radioName" className="data">Radio station name: </label>
          <input type="text" id="radioName" name="radioName" onChange={e =>updateRadioName(e.target.value)} 
            value={radioName}/>
      </div>
      <div className="container">
          <label htmlFor="startValue" className="data">Poti start value: </label>
          <input type="text" id="startValue" name="startValue" onChange={e =>updateMinimum(e.target.value)} value={minimum}/>
      </div>
      <div className="container">
          <label htmlFor="endValue" className="data">Poti end value: </label>
          <input type="text" id="endValue" name="endValue" onChange={e =>updateMaximum(e.target.value)} value={maximum}/>
      </div>
      <div className="container">
          <label htmlFor="url" className="data">Radio URL: </label>
          <input type="text" id="url" name="url" onChange={e =>updateUrl(e.target.value)} value={url}
            style={{color: urlState}}/>
      </div>
      <div className="container">
          <label htmlFor="radio_name_re" className="data">Radio name spare: </label>
          <input type="text" id="radio_name_re" name="radio_name_re" onChange={e =>updateRadioNameRe(e.target.value)} value={radioNameRe}/>
      </div>
      <div className="container">
          <label htmlFor="url_re" className="data">Radio URL spare: </label>
          <input type="text" id="url_re" name="url_re" onChange={e =>updateUrlRe(e.target.value)} 
          value={urlRe} style={{color: urlStateRe}}/>
      </div>
      <div className="container">
        <label htmlFor="re_active" className="data">Spare radio active: </label>
        <input type="checkbox" id="re_active" name="re_active" onChange={e =>updateReActive(e.target.checked)} 
          checked={reActive}/>        
      </div>
      <div className="container">
        <button type="button" onClick={testURL}>Test URL</button>
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
      <Button item={item} fetchFrequencies={props.fetchFrequencies} index={index} 
        selected={selectedButton === index} buttonClicked={setSelectedButton} setButton={props.setButton}
        testRunning={props.testRunning} setStopTest={props.setStopTest}/>
    </div>
  ));
};

function Button(props) {
  const buttonClick = () => {
    if (!props.testRunning) {
      props.setButton(props.item, props.index);
      props.fetchFrequencies(props.item);
      props.buttonClicked(props.index);
      
    } else {
      window.alert("TEST RUNNING");
      props.setStopTest(true);
    }
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
