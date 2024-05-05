from json import load
from time import sleep
import RPi.GPIO as GPIO

from Radio.db.db import Database


# BUG: This makes i2c non working
class ShutdownGpio:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.shutdown_pin = self.load_shutdown_pin()
        GPIO.setup(self.shutdown_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.db = Database()

    @staticmethod
    def load_shutdown_pin():
        with open('../data/settings.json') as f:
            settings = load(f)

        return settings["buttons"]["shutdown"]["pin"]

    def run(self):
        while True:
            GPIO.wait_for_edge(self.shutdown_pin, GPIO.FALLING)
            self.db.replace_shutdown(True)
            print("DETECTED SHUTDOWN")
            sleep(0.1)
