import sys
import os
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from Radio.util.util import is_raspberry, get_args, get_project_root
from Radio.radioDaemon import RadioDaemon

IS_RASPBERRY_PI = False
if is_raspberry():
    IS_RASPBERRY_PI = True
    mock = False
    import RPi.GPIO as GPIO


def stop():
    path_stop_file = get_project_root() / "stop.txt"
    with open(path_stop_file, "w") as file:
        file.write("stop")


if __name__ == "__main__":
    if IS_RASPBERRY_PI:
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
    try:
        daemon = RadioDaemon("", *get_args())
        if len(sys.argv) < 2:
            print("Usage: python main.py start|stop")
            sys.exit(1)
        if 'stop' == sys.argv[1]:
            stop()
        elif 'start' == sys.argv[1]:
            daemon._start()
        else:
            print(f"Unregocnized argument: {sys.argv[1]}")
    except KeyboardInterrupt:
        daemon._stop()
        sys.exit(0)
