import json
from threading import Event
import time
from statistics import mean
from time import sleep
from Radio.db.db import Database
from Radio.collector.gpio.button import RadioButtonsRaspi
from Radio.util.dataTransmitter import DataTransmitter
from Radio.util.sensorMsg import SensorMsg

from Radio.collector.ads1115.ads import AdsObject
from Radio.util.util import ThreadSafeInt, get_project_root, print_, ThreadSafeList

from Radio.util.util import is_raspberry

IS_RASBERRY = False
if is_raspberry():
    IS_RASBERRY = True


class Collector:
    def __init__(self, mock: bool = False, debug: bool = False, stop_event: Event=None, thread_stopped_counter: ThreadSafeInt=None,
                 amount_stop_threads_names: ThreadSafeList = None):
        self._stop_event: Event = stop_event
        self.debug: bool = debug
        self.thread_stopped_counter: ThreadSafeInt = thread_stopped_counter
        self.amount_stop_threads_names: ThreadSafeList = amount_stop_threads_names
        print_(debug=debug, class_name="Collector",
               text=f"START COLLECTING SENSOR VALUES WITH MOCK: {mock}")
        self.mock: bool = mock
        self.data_transmitter: DataTransmitter = DataTransmitter()

        self.buttons: RadioButtonsRaspi = RadioButtonsRaspi(mock=mock, debug=debug)
        self.ads = AdsObject(mock=mock, debug=debug)
        self.db = Database()
        self.cycle_time: float = 0
        self.load_from_settings()
        self.sensor_msg_old: SensorMsg = None
        print_(debug=debug, class_name="Collector", text="Collector started")

    
    def load_from_settings(self):
        with open(get_project_root() / 'data/settings.json') as f:
            settings = json.load(f)

        self.cycle_time = settings["cycle_time"]

    def run(self):
        cycle_time = 0.005
        while True:
            start = time.time()
            if not self.db.get_web_control_value():
                buttons_data = self.buttons.get_values()
                analog_data = self.ads.get()
                sensor_msg = SensorMsg()
                sensor_msg.set_buttons_data(buttons_data)
                sensor_msg.analog_data.set_data(analog_data.sensor_data)
                if self.sensor_msg_old != sensor_msg:
                    self.data_transmitter.send(sensor_msg)
                    self.sensor_msg_old = sensor_msg
                    # print("JO")
            if self._stop_event.is_set():
                self.thread_stopped_counter.increment()
                self.amount_stop_threads_names.delete(self.__class__.__name__)
                print("STOPPING COLLECTOR")
                break
            now = time.time()
            if cycle_time - (now - start) > 0:
                sleep(cycle_time - (now - start))


if __name__ == "__main__":
    collector = Collector(True)
    collector.run()
