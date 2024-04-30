from time import sleep
from Radio.db.db import Database
from Radio.util.RadioExceptions import SystemNotSupported
from Radio.gpio.button import RadioButtonsRaspi
from Radio.util.DataTransmitter import DataTransmitter
from Radio.sensorMsg import SensorMsg
from Radio.util.util import is_raspberry

from Radio.ads1115.ads import AdsObject


class Collector:
    def __init__(self, mock: bool = False):
        self.mock: bool = mock
        self.data_transmitter: DataTransmitter = DataTransmitter()

        self.buttons: RadioButtonsRaspi = RadioButtonsRaspi(mock=mock)
        self.ads = AdsObject(mock=mock)
        self.db = Database()

    def run(self):
        while True:
            if not self.db.get_web_control_value():
                buttons_data = self.buttons.get_values()
                analog_data = self.ads.get()
                sensor_msg = SensorMsg()
                sensor_msg.buttons_data.set_data(buttons_data)
                sensor_msg.analog_data.set_data(analog_data)
                self.data_transmitter.send(sensor_msg)
            sleep(0.0001)





if __name__ == "__main__":
    collector = Collector(True)
    collector.run()
