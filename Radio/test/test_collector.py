import time
import unittest
from multiprocessing import Process
from Radio.collector.collector import Collector
from Radio.util.sensorMsg import SensorMsg


class TestCollector(unittest.TestCase):
    @staticmethod
    def receive_and_print(collector):
        while True:
            data: SensorMsg = collector.data_transmitter.receive()
            buttons = data.buttons_data.get_data()
            analogs = data.analog_data.get_data_sensor()
            button_printable = []
            for button in buttons.sensor_data:
                button_printable.append({"pin": button.pin, "state": button.state, "states": button.state})
            analog_printable = []
            for analog in analogs.data:
                analog_printable.append({"pin": analog.pin, "value": analog.value})
            print(button_printable, analog_printable)
            time.sleep(1)

    def test_init(self):
        collector = Collector(True)
        p_send = Process(target=collector.run)
        p_recv = Process(target=self.receive_and_print, args=(collector,))

        p_send.start()
        p_recv.start()

        p_send.join()
        p_recv.join()