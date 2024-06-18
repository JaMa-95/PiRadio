import time
from statistics import mean
from time import sleep
from Radio.db.db import Database
from Radio.collector.gpio.button import RadioButtonsRaspi
from Radio.util.dataTransmitter import DataTransmitter
from Radio.util.sensorMsg import SensorMsg

from Radio.collector.ads1115.ads import AdsObject
from Radio.util.util import print_


class Collector:
    def __init__(self, mock: bool = False, debug: bool = False):
        self.debug: bool = debug
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


if __name__ == "__main__":
    collector = Collector(True)
    collector.run()
