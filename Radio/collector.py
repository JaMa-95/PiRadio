from time import sleep
from Radio.db.db import Database
from Radio.util.RadioExceptions import SystemNotSupported
from Radio.gpio.button import RadioButtonsRaspi
from Radio.util.DataTransmitter import DataTransmitter
from Radio.util.util import is_raspberry
if is_raspberry():
    is_raspberry = True
    from Radio.ads1115.ads import AdsObject
else:
    is_raspberry = False


class Collector:
    def __init__(self):
        self.data_transmitter: DataTransmitter = DataTransmitter()

        if is_raspberry:
            self.buttons: RadioButtonsRaspi = RadioButtonsRaspi()
            self.ads = AdsObject()
        else:
            self.ads = None
            self.buttons = None
        self.db = Database()

    def run(self):
        if not is_raspberry:
            raise SystemNotSupported("Not a raspberry pi or unsupported version")
        while True:
            if not self.db.get_web_control_value():
                buttons_data = self.buttons.get_values()
                analog_data = self.ads.get()
                self.data_transmitter.send({"buttons": buttons_data, "analog": analog_data})
            sleep(0.0001)


if __name__ == "__main__":
    collector = Collector()
    collector.run()