# ---------------------------------------------------
# Observer Pattern in publisher and subscriber model.
# ---------------------------------------------------
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
    print(f"path: {Path(__file__).parent}")
    return Path(__file__).parent.parent
