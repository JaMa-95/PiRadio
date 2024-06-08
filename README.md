# PiRadio
Build your own url streaming radio by connecting buttons and potentiometers to your raspberry pi.
Use the webapp to change to settings or control the radio from any device.

# Known Issues
- Raspbian OS Lite not working because of VLC player. 
- make Software run as a service. Not working because sound is played with user rights

# Hardware
- Optional: print [PCB](PCB) 
- assembly components according to PCB layout

# Installation
- enable I2C
## packages
- sudo apt update
- sudo apt upgrade
- sudo apt install python3-pip
- sudo apt install npm 

- python -m ./Radio/venv ./Radio/venv
- pip install -r ./Radio/requirements.txt
- pip install RPi.GPIO
- pip install adafruit-blinka
- pip install adafruit-circuitpython-ads1x15
- npm --prefix ./Radio/react-app install ./Radio/react-app

- cp Radio/radio.sh  /etc/profile.d/radioStart.sh

## mpd
edit file /etc/mpd.conf
```commandline
    # An example of an ALSA output:
    #       
    audio_output {
            type            "alsa"
            name            "My ALSA Device"
    #       device          "hw:0,0"        # optional
            mixer_type      "software"      # optional
    #       mixer_device    "default"       # optional
    #       mixer_control   "PCM"           # optional
    #       mixer_index     "0"             # optional
    }
```

# autostart
https://raspberrypi.stackexchange.com/questions/40415/how-to-enable-auto-login
https://unix.stackexchange.com/questions/56083/how-to-write-a-shell-script-that-gets-executed-on-login

### service is no working because of user rights which are needed to interact with audio
sudo nano /lib/systemd/system/radio.service

https://unix.stackexchange.com/questions/56083/how-to-write-a-shell-script-that-gets-executed-on-login

# TODO
logarithmic poti

# react
npm install react-bootstrap bootstrap

# ADS1x15
https://learn.adafruit.com/adafruit-4-channel-adc-breakouts/python-circuitpython

# Pontentiometer
Low-Pass Filter with 100yF Capacitor and 47k Ohm Resistance -> frequencies
Low-Pass Filter with 22yF Capacitor and 47k Ohm Resistance -> volume -> must be faster
https://www.instructables.com/Smooth-Potentiometer-Input/

# ERROR
## Segmentation fault
https://stackoverflow.com/questions/10035541/what-causes-a-python-segmentation-fault


# helpful links
https://learn.adafruit.com/adafruit-i2s-stereo-decoder-uda1334a/raspberry-pi-usage
https://raspberrypi.stackexchange.com/questions/639/how-to-get-pulseaudio-running
https://pimylifeup.com/raspberry-pi-vlc/