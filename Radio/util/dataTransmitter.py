from multiprocessing import Pipe


class DataTransmitter:
    def __init__(self):
        self.parent_conn, self.child_conn = Pipe()

    def send(self, data):
        self.child_conn.send(data)

    def receive(self):
        data = self.parent_conn.recv()
        return data

    def has_data(self):
        return self.parent_conn.poll()
