# Shutdown Helper Script
#
# Watchdog function:
# Pi watches for a short low pulse on GPIO and responds
# with its own short low pulse.
#
# Shutdown is requested by pulling GPIO pin 4 low for 1 sec.
# The rquest is acknowledged by setting GPIO 4 as an output
# and setting it low.
import json
import time
import subprocess

from Radio.raspberry.raspberry import Raspberry
from Radio.util.util import get_project_root, is_raspberry
IS_RASPBERRY = False
if is_raspberry():
    IS_RASPBERRY = True
    import RPi.GPIO as GPIO


class OnOffButton:
    def __init__(self):
        self.active_pin: int = 0
        self.poll_pin: int = 0
        if IS_RASPBERRY:
            self.raspberry: Raspberry = Raspberry()
            self.load_settings()

        print("STARTUP ON")

    def load_settings(self):
        with open(get_project_root() / 'data/settings.json') as f:
            settings = json.load(f)
        self.active_pin = settings["on_off_button"]["active_pin"]
        self.poll_pin = settings["on_off_button"]["poll_pin"]

    def activate_pin(self):
        GPIO.setup(self.poll_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.active_pin, GPIO.OUT)
        GPIO.output(self.active_pin, GPIO.HIGH)

    def run(self):
        if IS_RASPBERRY:
            while True:
                GPIO.wait_for_edge(self.poll_pin, GPIO.FALLING)
                start = time.time()
                while not GPIO.input(self.poll_pin):
                    time.sleep(0.01)

                if time.time() - start < 0.1:
                    self.poll(start)
                else:
                    print("Shutdown request detected\n")
                    self.acknowledge()
                    self.raspberry.turn_raspi_off()

    def poll(self, start):
        GPIO.setup(self.poll_pin, GPIO.OUT, initial=0)
        time.sleep(0.05)
        GPIO.setup(self.poll_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        print("Poll ")
        print(time.time() - start)
        print("\n")

    def acknowledge(self):
        # Acknowledge by setting the GPIO pin as Output, Low
        GPIO.setup(self.poll_pin, GPIO.OUT)
        GPIO.output(self.poll_pin, GPIO.LOW)
        time.sleep(0.01)
        GPIO.output(self.poll_pin, GPIO.HIGH)
        GPIO.setup(self.poll_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

