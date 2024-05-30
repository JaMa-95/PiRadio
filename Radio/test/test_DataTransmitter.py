import unittest
from multiprocessing import Process
from threading import Thread

from Radio.util.dataTransmitter import DataTransmitter
from Radio.util.sensorMsg import SensorMsg


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

    def test_thread(self):
        data_transmitter = DataTransmitter()
        data_receiver = DataTransmitter()
        msg = SensorMsg()
        thread = Thread(target=data_transmitter.send, args=(msg, ))
        thread.start()
        data = data_receiver.receive()
        self.assertTrue(isinstance(data, SensorMsg))
