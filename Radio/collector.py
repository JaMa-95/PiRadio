from time import sleep

from button import RadioButtonsRaspi
from ads import AdsObject


class Collector:
    def __init__(self):
        self.buttons = RadioButtonsRaspi()
        self.ads = AdsObject()

    def run(self):
        while True:
            self.buttons.set_values_to_db()
            self.ads.set_to_db()
            sleep(0.01)
