#!/bin/bash
MODULE_PATH="~/Code/PiRadio"
PID_FILE="/var/run/PiRadio.pid"

WEB_APP_PATH="home/jakob/Code/PiRadio/Radio/react-app"

start() {
    if [ -f $PID_FILE ]; then
        echo "The service is already running."
    else
        cd $MODULE_PATH
        source Radio/venv/bin/activate
        # python -m Radio.main --app=1 
        echo $! > $PID_FILE
        npm start --prefix Radio/react-app
        echo "Service started."
    fi
}

stop() {
    if [ -f $PID_FILE ]; then
        kill $(cat $PID_FILE)
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