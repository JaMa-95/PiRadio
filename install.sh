#!/bin/bash 

# check if script is run as root
raspi-config nonint do_i2c 0

apt update
apt upgrade
apt install python3-pip

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
PI_RADIO_SERVICE_PATH="PiRadio.service"
APP_PLACEHOLDER_TEXT="--app=0"
while true; do
    read -p "Do you want to install web frontend?" yn
    case $yn in
        [Yy]* ) apt install npm; 
        sed -i  "s,$APP_PLACEHOLDER_TEXT,--app=1,g" $PI_RADIO_SERVICE_PATH
                break;;
        [Nn]* ) break;
        * ) echo "Please answer yes or no.";;
    esac
done

python -m ./Radio/venv ./Radio/venv
source ./Radio/venv/bin/activate
# install raspberry dependent packages
pip install -r ./Radio/requirements.txt
pip install adafruit-blinka
pip install adafruit-circuitpython-ads1x15
pip install smbus
pip install rpi-lgpio


# exchange home path in service file
HOMEDIRPATH_PLACEHOLDER_PATH="PATH_TO_PIRADIO"
sed -i  "s,$HOMEDIRPATH_PLACEHOLDER_PATH,$SCRIPT_DIR,g" $PI_RADIO_SERVICE_PATH

# exchange name in service file
USERNAME_PLACEHOLDER="USERNAME"
USERNAME=$(whoami)
sed -i  "s,$USERNAME_PLACEHOLDER,$USERNAME,g" $PI_RADIO_SERVICE_PATH


# copy service file to /etc/systemd/system
SYSTEM_SERVICE_PATH=$SCRIPT_DIR + "/PiRadio.service"
cp $SYSTEM_SERVICE_PATH  /etc/systemd/system/

systemctl enable mpd