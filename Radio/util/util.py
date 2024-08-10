# ---------------------------------------------------
# Observer Pattern in publisher and subscriber model.
# ---------------------------------------------------
import os
import io
from pathlib import Path
import sys
import threading
import subprocess


def react_app_start():
    root = get_project_root() / "react-app"
    subprocess.Popen(f"cd {root} && npm start", shell=True)


class ThreadSafeInt:
    def __init__(self, value=0):
        self._value = value
        self._lock = threading.Lock()

    def increment(self):
        with self._lock:
            self._value += 1

    def get(self):
        with self._lock:
            return self._value


class Singleton(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print('Creating the object')
            cls._instance = super(Singleton, cls).__new__(cls)
            # Put any initialization here.
        return cls._instance



def get_args(mock_=False, collector_on_=True, sole_web_control_=False, debug_=False, app_=True):
    if len(sys.argv) > 1:
        for arg in sys.argv:
            if arg == "--collector=0":
                collector_on_ = False
            if arg == "--sole_web=1":
                sole_web_control_ = True
            if arg == "--mock=1":
                mock_ = True
            if arg == "--debug=1":
                debug_ = True
            if arg == "--app=0":
                app_ = False
    return mock_, collector_on_, sole_web_control_, debug_, app_

def get_project_root() -> Path:
    return Path(__file__).parent.parent


def map_(max_a: int, min_a: int,  max_b: int, min_b: int, value: int):
    return (value - min_a) / (max_a - min_a) * (max_b - min_b) + min_b


def is_raspberry() -> bool:
        try:
            with io.open('/sys/firmware/devicetree/base/model', 'r') as m:
                if 'raspberry pi' in m.read().lower(): return True
        except Exception: pass
        return False


def print_(debug: bool, text: str, class_name: str = ""):
    if debug:
        if class_name:
            print(f"{class_name}: {text}")
        else:
            print(text)
