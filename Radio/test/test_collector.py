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

    def test_analog(self, collector: Collector):
        pins_to_print = [3]
        while True:
            data: SensorMsg = collector.data_transmitter.receive()
            analogs = data.analog_data.get_data_sensor()
            analog_printable = []
            for analog in analogs:
                if analog.pin not in pins_to_print:
                    continue
                analog_printable.append({"pin": analog.pin, "value": analog.value})
            print(analog_printable)
            time.sleep(1)

    def test_run_analog(self):
        mock = False
        collector = Collector(mock)
        p_send = Process(target=collector.run)
        p_recv = Process(target=self.test_analog, args=(collector,))

        p_send.start()
        p_recv.start()

        p_send.join()
        p_recv.join()

    def test_init(self):
        mock = False
        collector = Collector(mock)
        p_send = Process(target=collector.run)
        p_recv = Process(target=self.receive_and_print, args=(collector,))

        p_send.start()
        p_recv.start()

        p_send.join()
        p_recv.join()


if __name__ == '__main__':
    tester = TestCollector()
    tester.test_run_analog()