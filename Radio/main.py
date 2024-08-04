import sys
import os

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
    daemon = RadioDaemon("/tmp/PiRadio.pid", *get_args())
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            # we cannot stop the daemon from the daemon itself, because of threads
            stop()
            # daemon.stop()
        elif 'restart' == sys.argv[1]:
            stop()
            # daemon.stop()
            daemon.start()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)
