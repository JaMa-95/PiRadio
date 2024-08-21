# PiRadio
Build your own web streaming radio by connecting buttons and potentiometers to your raspberry pi.
Use the webserver to change settings or control the radio from any device.

# TODO
- support logarithmic poti
- run as service
- test with raspberry pi zero
- automatic audio driver settings
- create install script

# Hardware
- Raspberry Pi 4 (Others should work the same)
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
- pip install smbus

 [reason for uninstall install](https://stackoverflow.com/questions/78386891/raspberry-pi-4-python-runtimeerror-error-waiting-for-edge)
- pip uninstall rpi.gpio
- pip install rpi-lgpio

prefer using already available node modules. Raspberry takes a long time installing packages
- npm --prefix ./Radio/react-app install ./Radio/react-app

- cp Radio/radio.sh  /etc/profile.d/radioStart.sh

# audio
## mpd
edit file /etc/mpd.conf

When using aux ouput or comment out when using uda1334
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
## uda1334
[Installation guide](https://learn.adafruit.com/adafruit-i2s-stereo-decoder-uda1334a/raspberry-pi-usage)

# autostart
https://raspberrypi.stackexchange.com/questions/40415/how-to-enable-auto-login
https://unix.stackexchange.com/questions/56083/how-to-write-a-shell-script-that-gets-executed-on-login

# service 
sudo nano /lib/systemd/system/radio.service

# ERROR
## Segmentation fault
https://stackoverflow.com/questions/10035541/what-causes-a-python-segmentation-fault


# helpful links
https://learn.adafruit.com/adafruit-i2s-stereo-decoder-uda1334a/raspberry-pi-usage
https://raspberrypi.stackexchange.com/questions/639/how-to-get-pulseaudio-running
https://pimylifeup.com/raspberry-pi-vlc/
