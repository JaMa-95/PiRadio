#!/bin/bash 
raspi-config nonint do_i2c 0

apt update
apt upgrade
apt install python3-pip

while true; do
    read -p "Do you want to install web frontend?" yn
    case $yn in
        [Yy]* ) apt install npm; break;;
        [Nn]* ) break;
        * ) echo "Please answer yes or no.";;
    esac
done

python -m ./Radio/venv ./Radio/venv
pip install -r ./Radio/requirements.txt
pip install adafruit-blinka
pip install adafruit-circuitpython-ads1x15
pip install smbus
pip install rpi-lgpio
systemctl enable mpd
# TODO: change radio.sh paths dynamically
