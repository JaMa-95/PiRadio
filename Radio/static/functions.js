function rePosition() {
    const checked = document.getElementById("toggleWebControl").checked;
    if (!checked)
    {
        var value = Number(document.getElementById("valueLang").innerText);
        document.getElementById("sliderRadio").value = value;
    }
}

function updateVolume() {
    const checked = document.getElementById("toggleWebControl").checked;
    if (!checked)
    {
        var value = Number(document.getElementById("valueVolume").innerText);
        document.getElementById("volumeKnob").value = value;
    }
}

function changeImage(elementId, value) {
    var element = document.getElementById(elementId);
    if (value == 1 || value == "On")
    {
        element.style.visibility = 'hidden';
    }
    else if (value == 0 || value == "Off") {
        element.style.visibility = 'visible';
    }
    else {
        // console.log("Error at buttons value");
    }
}

function rePositionButtons() {
        var value = Number(document.getElementById("buttonOn").innerText);
        changeImage("on_off", value);
        value = Number(document.getElementById("buttonLang").innerText);
        changeImage("lang_off", value);
        value = Number(document.getElementById("buttonMittel").innerText);
        changeImage("mittel_off", value);
        value = Number(document.getElementById("buttonKurz").innerText);
        changeImage("kurz_off", value);
        value = Number(document.getElementById("buttonUkw").innerText);
        changeImage("ukw_off", value);
        value = Number(document.getElementById("buttonSpr").innerText);
        changeImage("spr_off", value);
}

function waitForElementToDisplay(selector, callback, checkFrequencyInMs, timeoutInMs) {
  var startTimeInMs = Date.now();
  (function loopSearch() {
    if (document.querySelector(selector) != null) {
      callback();
      return;
    }
    else {
      setTimeout(function () {
        if (timeoutInMs && Date.now() - startTimeInMs > timeoutInMs)
          return;
        loopSearch();
      }, checkFrequencyInMs);
    }
  })();
}


waitForElementToDisplay("#valueLang",function(){
    const elm = document.getElementById("valueLang");
    if (elm) {
        var intervalId = window.setInterval(function(){
          rePosition();
          rePositionButtons();
          updateVolume();
        }, 300);
    }
},1000,9000);

function hello()
{
    alert("Hello World");
}

function sendWebControlValue(checkbox)
{
    const value = checkbox.checked;
    const formData = new FormData();
    formData.append("state", value);
    document.getElementById("volumeKnob").disabled = !value;

    fetch("/web_control", {
        method: "POST",
        body: formData
    }).then();
}

function sendPosValue(value)
{
    const checked = document.getElementById("toggleWebControl").checked;
    if (checked)
    {
        var url = "/pos_lang_kurz_mittel/" + value
        fetch(url, {
            method: "GET"
        }).then();
    }
}

function buttonClicked(buttonName, state)
{
    const checked = document.getElementById("toggleWebControl").checked;
    if (checked)
    {
        changeImage(buttonName, state);
        var url = "/button_clicked/" + buttonName + "/" + state
        fetch(url, {
            method: "GET"
        }).then();
    }
}

function sendVolume(volumeKnob)
{
    const checked = document.getElementById("toggleWebControl").checked;
    if (checked)
    {
        const value = volumeKnob.value;
        alert(value);
        var url = "/volume/" + value
        fetch(url, {
            method: "GET"
        }).then();
    }
}