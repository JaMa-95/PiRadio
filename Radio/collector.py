from time import sleep

from button import RadioButtonsRaspi
from ads1115.ads import AdsObject


class Collector:
    def __init__(self):
        self.buttons = RadioButtonsRaspi()
        self.ads = AdsObject()

    def run(self):
        self.buttons.set_values_to_db()
        self.ads.set_to_db()
        sleep(0.01)
