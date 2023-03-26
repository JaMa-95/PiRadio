# ---------------------------------------------------
# Observer Pattern in publisher and subscriber model.
# ---------------------------------------------------
from abc import ABC, abstractmethod

class Publisher:
    def __init__(self):
        self.__subscribers = []
        self.__content = None

    def attach(self, subscriber):
        self.__subscribers.append(subscriber)

    def detach(self):
        self.__subscribers.pop()

    def get_subscribers(self):
        return[type(x).__name__ for x in self.__subscribers]

    def updateSubscribers(self):
        for sub in self.__subscribers:
            sub.update()

    def add_content(self, content):
        self.__content = content

    def get_content(self):
        return ("Content:" + self.__content)

# -------------------------------------
# Subscriber base class
# -------------------------------------
class Subscriber(ABC):

    @abstractmethod
    def update(self):
        pass

# --------------------
# Subscriber 1
# --------------------
class SiteSubscriber(Subscriber):
    def __init__(self, publisher):
        self.publisher = publisher
        self.publisher.attach(self)

    def update(self):
        print(type(self).__name__, self.publisher.get_content())

# --------------------
# Subscriber 2
# --------------------
class IntranetSubscriber(Subscriber):
    def __init__(self, publisher):
        self.publisher = publisher
        self.publisher.attach(self)

    def update(self):
        print(type(self).__name__, self.publisher.get_content())

# --------------------
# Subscriber 3
# --------------------
class ApiSubscriber(Subscriber):
    def __init__(self, publisher):
        self.publisher = publisher
        self.publisher.attach(self)

    def update(self):
        print(type(self).__name__, self.publisher.get_content())


def get_value_smoothed():
    values = []
    for i in range(100):
        values.append(100)

    value_smoothed = 0
    for value in values:
        value_smoothed += value
    print(f"new value {value}")
    return value_smoothed / len(values)

from ads import AdsObject

adsO = AdsObject()

while True:
    values = []
    for i in range(50):
        values.append(adsO.mittel_poti.get_value())
    print(f"{min(values)} : {max(values) : {max(values) - min(values)}}")


