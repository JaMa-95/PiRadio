# Radio
Using python and vlc player to stream music from online radios. Using the IO-Pins and potentiometers to change switch between radio streams.
Additionally add led strip to highlight the current used settings.

Use the webapp to change to settings or control the radio.

# Known Issues
- Raspbian OS Lite not working because of VLC player. 
-  make Software run as a service. Not working because sound is playing with user rights

  
# helpful links

https://learn.adafruit.com/adafruit-i2s-stereo-decoder-uda1334a/raspberry-pi-usage
https://raspberrypi.stackexchange.com/questions/639/how-to-get-pulseaudio-running
https://pimylifeup.com/raspberry-pi-vlc/

# autostart

## this is working
 /etc/profile.d/radioStart.sh

 
https://raspberrypi.stackexchange.com/questions/40415/how-to-enable-auto-login
https://unix.stackexchange.com/questions/56083/how-to-write-a-shell-script-that-gets-executed-on-login

## not working
https://raspberrypi.stackexchange.com/questions/108694/how-to-start-a-python-script-at-boot

### service is no working because of user rights which are needed to interact with audio
sudo nano /lib/systemd/system/radio.service

# Power up
https://embeddedcomputing.com/technology/open-source/development-kits/raspberry-pi-power-up-and-shutdown-with-a-physical-button

# LED
https://dordnung.de/raspberrypi-ledstrip/ws2812

# AUDIO
sudo adduser root pulse-access

To run pythons script and pulseAudio with root access. Root access is needed by ws2811 led strip. Pulse Audio is by default not usable from root

# ADS1x15
https://learn.adafruit.com/adafruit-4-channel-adc-breakouts/python-circuitpython

# Pontentiometer
Low-Pass Filter with 100yF Capacitor and 47k Ohm Resistance -> frequencies
Low-Pass Filter with 22yF Capacitor and 47k Ohm Resistance -> volume -> must be faster
https://www.instructables.com/Smooth-Potentiometer-Input/

# ERROR
## Segmentation fault
https://stackoverflow.com/questions/10035541/what-causes-a-python-segmentation-fault

# DEPENDENCIES

- sudo apt update
- sudo apt upgrade
- sudo apt install python3-pip
- sudo apt install pulseaudio   # for vlc

- sudo pip install adafruit-circuitpython-ads1x15
- sudo pip install paho-mqtt
- sudo pip install python-vlc
- sudo pip install fastapi
- sudo pip install uvicorn

- sudo apt install npm
- npm install react-bootstrap bootstrap


Depence on led strip
- sudo pip install rpi-ws281x
## deprecated
- sudo pip install Flask-Cors
- sudo pip install Turbo-Flask

# radioStart.sh

#!/bin/bash
# only works when autologin
#touch /home/pi/hello.txt
#export PATH=/usr/local/bin:/bin:/usr/bin:/sbin:/usr/sbin
cd /home/pi/PiRadio
#git pull
sleep 1
for pid in $(pidof -x radioStart.sh); do
    if [ $pid != $$ ]; then
        echo "already running"
        exit 1
    fi
done
echo "start script"
sudo python /home/pi/PiRadio/Radio/main.py &>  cat /home/pi/log.log

