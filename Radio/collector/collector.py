from threading import Event
import time
from statistics import mean
from time import sleep
from Radio.db.db import Database
from Radio.collector.gpio.button import RadioButtonsRaspi
from Radio.util.dataTransmitter import DataTransmitter
from Radio.util.sensorMsg import SensorMsg

from Radio.collector.ads1115.ads import AdsObject
from Radio.util.util import ThreadSafeInt, print_


class Collector:
    def __init__(self, mock: bool = False, debug: bool = False, stop_event: Event=None, thread_stopped_counter: ThreadSafeInt=None):
        self._stop_event: Event = stop_event
        self.debug: bool = debug
        self.thread_stopped_counter: ThreadSafeInt = thread_stopped_counter
        print_(debug=debug, class_name="Collector",
               text=f"START COLLECTING SENSOR VALUES WITH MOCK: {mock}")
        self.mock: bool = mock
        self.data_transmitter: DataTransmitter = DataTransmitter()

        self.buttons: RadioButtonsRaspi = RadioButtonsRaspi(mock=mock, debug=debug)
        self.ads = AdsObject(mock=mock, debug=debug)
        self.db = Database()
        print_(debug=debug, class_name="Collector", text="Collector started")

    def run(self):
        while True:
            if not self.db.get_web_control_value():
                buttons_data = self.buttons.get_values()
                analog_data = self.ads.get()
                sensor_msg = SensorMsg()
                sensor_msg.set_buttons_data(buttons_data)
                sensor_msg.analog_data.set_data(analog_data.sensor_data)
                self.data_transmitter.send(sensor_msg)
            if self._stop_event.is_set():
                self.thread_stopped_counter.increment()
                print("STOPPING COLLECTOR")
                break


if __name__ == "__main__":
    collector = Collector(True)
    collector.run()
