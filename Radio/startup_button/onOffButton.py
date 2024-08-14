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
from threading import Event
import time

from Radio.raspberry.raspberry import Raspberry
from Radio.util.util import ThreadSafeInt, get_project_root, is_raspberry
IS_RASPBERRY = False
if is_raspberry():
    IS_RASPBERRY = True
    import RPi.GPIO as GPIO


class OnOffButton:
    def __init__(self, stop_event: Event, thread_stopped_counter: ThreadSafeInt):
        self._stop_event = stop_event
        self.thread_stopped_counter = thread_stopped_counter
        self.active_pin: int = 5
        self.poll_pin: int = 22
        if IS_RASPBERRY:
            self.raspberry: Raspberry = Raspberry()
            # self.load_settings()
            self.activate_pins()

        print("ON/OFF Button active")

    def load_settings(self):
        with open(get_project_root() / 'data/settings.json') as f:
            settings = json.load(f)
        self.active_pin = settings["on_off_button"]["active_pin"]
        self.poll_pin = settings["on_off_button"]["poll_pin"]

    def activate_pins(self):
        GPIO.setup(self.poll_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.active_pin, GPIO.OUT)
        #GPIO.output(self.active_pin, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(self.active_pin, GPIO.HIGH)
    
    def check_(self, _):
        start = time.time()
        while not GPIO.input(self.poll_pin):
            if self._stop_event.is_set():
                break
            time.sleep(0.01)

        if time.time() - start < 0.1:
            self.poll(start)
            GPIO.add_event_callback(self.poll_pin, self.check_)
        else:
            print("Shutdown request detected\n")
            self.acknowledge()
            GPIO.setup(self.active_pin, GPIO.OUT)
            GPIO.output(self.active_pin, GPIO.LOW)
            self.raspberry.turn_raspi_off()

    def run(self):
        if IS_RASPBERRY:
            GPIO.add_event_detect(self.poll_pin, GPIO.FALLING)
            GPIO.add_event_callback(self.poll_pin, self.check_)
            while not self._stop_event.is_set():
                time.sleep(1)
        self.thread_stopped_counter.increment()
        print("ON/OFF Button stopped")

    def poll(self, start):
        GPIO.setup(self.poll_pin, GPIO.OUT, initial=0)
        time.sleep(0.05)
        GPIO.setup(self.poll_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        print("Poll: ", time.time() - start)

    def acknowledge(self):
        # Acknowledge by setting the GPIO pin as Output, Low
        GPIO.setup(self.poll_pin, GPIO.OUT)
        GPIO.output(self.poll_pin, GPIO.LOW)
        time.sleep(0.01)
        GPIO.output(self.poll_pin, GPIO.HIGH)
        GPIO.setup(self.poll_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

