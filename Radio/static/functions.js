function rePosition() {
        let value = Number(document.getElementById("valueLang").innerText);
        var elem = document.getElementById('redLine');
        let startPixel = 350;
        let endPixel = 912;
        let startValue = 3000;
        let endValue = 1850;

        let movePercent = (value - endValue) / (startValue - endValue);
        let movePixels = movePercent * (endPixel - startPixel);
        let movePixelString = movePixels.toString() + 'px';
        $(elem).animate({ 'left': movePixelString });
}

function changeImage(elementId, value) {
    var element = document.getElementById(elementId);
    if (value == 1)
    {
        element.style.visibility = 'hidden';
    }
    else {
        element.style.visibility = 'visible';
    }
}

function rePositionButtons() {
        let value = Number(document.getElementById("buttonOn").innerText);
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
        }, 300);
    }
},1000,9000);

function hello()
{
    document.getElementById("button").style.color = "red"
}