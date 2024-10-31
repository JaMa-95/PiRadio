from abc import ABC, abstractmethod
from multiprocessing import Pipe
from multiprocessing.connection import wait

from Radio.util.singleton import Singleton


class DataTransmitter(Singleton):
    def __init__(self):
        self.parent_conn, self.child_conn = Pipe()

    def send(self, data):
        self.child_conn.send(data)

    def receive(self):
        data = self.parent_conn.recv()
        return data

    def has_data(self):
        return self.parent_conn.poll()
    
    def wait_for_data(self, timeout: bool=1):
        wait([self.parent_conn], timeout=timeout)
        if self.has_data():
            return self.receive()
        return None


class Publisher(Singleton):
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
        return self.__content

    def publish(self, data):
        self.add_content(data)
        self.update_subscribers()


class Subscriber(ABC):

    @abstractmethod
    def update(self):
        pass
