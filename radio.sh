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
npm start --prefix /home/pi/PiRadio/Radio/react-app