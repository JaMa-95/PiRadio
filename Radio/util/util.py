# ---------------------------------------------------
# Observer Pattern in publisher and subscriber model.
# ---------------------------------------------------
import os
import io
from pathlib import Path


class Singleton(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print('Creating the object')
            cls._instance = super(Singleton, cls).__new__(cls)
            # Put any initialization here.
        return cls._instance


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
