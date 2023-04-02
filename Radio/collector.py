from time import sleep

from button import RadioButtonsRaspi
from ads import AdsObject
from db import db

class Collector:
    def __init__(self):
        self.buttons = RadioButtonsRaspi()
        self.ads = AdsObject()
        self.db = db

    def run(self):
        while True:
            if self.db.get_web_contro_value():
                self.buttons.set_values_to_db()
                self.ads.set_to_db()
            sleep(0.005)
