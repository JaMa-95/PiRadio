from multiprocessing import Pipe

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
