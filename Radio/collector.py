from time import sleep

from button import RadioButtonsRaspi
from ads import AdsObject
from db.db import Database


class Collector:
    def __init__(self):
        self.buttons = RadioButtonsRaspi()
        self.ads = AdsObject()
        self.db = Database()

    def run(self):
        while True:
            if not self.db.get_web_control_value():
                self.buttons.set_values_to_db()
                self.ads.set_to_db()
            sleep(0.00001)
