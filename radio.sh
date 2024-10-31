#!/bin/bash
MODULE_PATH="/home/jakob/Code/PiRadio/"
#MODULE_PATH=MODULE_PLACEHOLDER_PATH
# PID_FILE="/var/run/PiRadio.pid"
PID_FILE="/home/jakob/Code/PiRadio/PiRadio.pid"
    

start() {
    source Radio/venv/bin/activate
    python -m Radio.main start
}

stop() {
    source Radio/venv/bin/activate
    python -m Radio.main stop
}

restart() {
    python -m Radio.main restart
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
