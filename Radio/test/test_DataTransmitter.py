import unittest
from multiprocessing import Process
from Radio.util.dataTransmitter import DataTransmitter


class TestDataTransmitter(unittest.TestCase):
    def test_init(self):
        data_transmitter = DataTransmitter()

    def test_send(self):
        data_transmitter = DataTransmitter()
        data_transmitter.send("Hello World!")

    def test_send_recv(self):
        data_transmitter = DataTransmitter()
        data_transmitter.send("Hello World!")
        recv = data_transmitter.receive()
        self.assertEqual(recv, "Hello World!")

    def test_processes(self):
        data_transmitter = DataTransmitter()
        p = Process(target=data_transmitter.send, args=("Hello World!",))
        p.start()
        data = data_transmitter.receive()
        p.join()
        self.assertEqual(data, "Hello World!")
