#!/bin/bash
VENV_PATH="/home/pi/PiRadio/Radio/venv/bin/activate"
APP_PATH="/home/pi/PiRadio/Radio/main.py"
PID_FILE="/var/run/PiRadio.pid"

WEB_APP_PATH="/home/pi/PiRadio/react-app"

start() {
    if [ -f $PID_FILE ]; then
        echo "The service is already running."
    else
        source $VENV_PATH
        nohup python3 $APP_PATH &> /dev/null &
        echo $! > $PID_FILE
        npm start --prefix $WEB_APP_PATH &
        echo "Service started."
    fi
}

stop() {
    if [ -f $PID_FILE ]; then
        kill $(cat $PID_FILE)
        rm $PID_FILE
        npm stop --prefix $WEB_APP_PATH
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