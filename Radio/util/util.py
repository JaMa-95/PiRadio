# ---------------------------------------------------
# Observer Pattern in publisher and subscriber model.
# ---------------------------------------------------
import os
import io
from abc import ABC, abstractmethod
from pathlib import Path


class Publisher:
    def __init__(self):
        self.__subscribers = []
        self.__content = None

    def attach(self, subscriber):
        self.__subscribers.append(subscriber)

    def detach(self):
        self.__subscribers.pop()

    def get_subscribers(self):
        return [type(x).__name__ for x in self.__subscribers]

    def update_subscribers(self):
        for sub in self.__subscribers:
            sub.update()

    def add_content(self, content):
        self.__content = content

    def get_content(self):
        return "Content:" + self.__content


# -------------------------------------
# Subscriber base class
# -------------------------------------
class Subscriber(ABC):

    @abstractmethod
    def update(self):
        pass


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


def is_raspberry() -> bool:
    if os.name != 'posix':
        return False
    chips = ('BCM2708', 'BCM2709', 'BCM2711', 'BCM2835', 'BCM2836')
    try:
        with io.open('/proc/cpuinfo', 'r') as cpuinfo:
            for line in cpuinfo:
                if line.startswith('Hardware'):
                    _, value = line.strip().split(':', 1)
                    value = value.strip()
                    if value in chips:
                        return True
    except Exception:
        pass
    return False
