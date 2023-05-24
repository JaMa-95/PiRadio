# Radio


https://learn.adafruit.com/adafruit-i2s-stereo-decoder-uda1334a/raspberry-pi-usage
https://raspberrypi.stackexchange.com/questions/639/how-to-get-pulseaudio-running
https://pimylifeup.com/raspberry-pi-vlc/

# not working
https://raspberrypi.stackexchange.com/questions/108694/how-to-start-a-python-script-at-boot


# service is no working because of user rights which are needed to interact with audio
sudo nano /lib/systemd/system/radio.service

# this is working
https://raspberrypi.stackexchange.com/questions/40415/how-to-enable-auto-login
https://unix.stackexchange.com/questions/56083/how-to-write-a-shell-script-that-gets-executed-on-login



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
sudo pip install adafruit-circuitpython-ads1x15
sudo pip install paho-mqtt
sudo pip install adafruit-circuitpython-ads1x15

Depence on led strip
sudo pip install rpi-ws281x
##deprecated
sudo pip install Flask-Cors
sudo pip install Turbo-Flask

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

