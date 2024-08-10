import sys
import os
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from Radio.util.util import is_raspberry, get_args, get_project_root
from Radio.radioDaemon import RadioDaemon

if is_raspberry():
    IS_RASPBERRY_PI = True
    mock = False


def stop():
    path_stop_file = get_project_root() / "stop.txt"
    with open(path_stop_file, "w") as file:
        file.write("stop")


if __name__ == "__main__":
    try:
        daemon = RadioDaemon("", *get_args())
        if len(sys.argv) < 2:
            print("Usage: python main.py start|stop")
            sys.exit(1)
        if 'stop' == sys.argv[1]:
            stop()
        elif 'start' == sys.argv[1]:
            daemon._start()
    except KeyboardInterrupt:
        daemon._stop()
        sys.exit(0)
