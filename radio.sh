#!/bin/bash
MODULE_PATH="/home/jakob/Code/PiRadio/"
#MODULE_PATH=MODULE_PLACEHOLDER_PATH
# PID_FILE="/var/run/PiRadio.pid"
PID_FILE="/home/jakob/Code/PiRadio/PiRadio.pid"

start() {
    if [ -f $PID_FILE ]; then
        echo "The service is already running."
    else
        cd $MODULE_PATH
        source Radio/venv/bin/activate
        python -m Radio.main  --mock=1 #--app=0 --collector=1 
        echo "STARTED RADIO"
        nohup npm start --prefix Radio/react-app &
        echo "STARTED WEBSERVER"
        echo $! > $PID_FILE
        echo "Service started."
    fi
}

stop() {
    if [ -f $PID_FILE ]; then
        # this stops the python script
        echo "stop" > $MODULE_PATH/stop.txt
        rm $PID_FILE
        cd $MODULE_PATH
        npm stop --prefix Radio/react-app
        echo "Service stopped."
    else
        echo "The service is not running."
    fi
}

restart() {
    stop
    start
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
esac
