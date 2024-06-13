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

# exchange name in start script
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
RADIO_SH_PATH="install.sh"
MODULE_PLACEHOLDER_PATH="MODULE_PLACEHOLDER_PATH"
sed -i  "s,$MODULE_PLACEHOLDER_PATH,$SCRIPT_DIR,g" $RADIO_SH_PATH