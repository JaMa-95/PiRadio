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
import os

from Radio.raspberry.raspberry import Raspberry
from Radio.util.util import ThreadSafeInt, get_project_root, is_raspberry, ThreadSafeList
IS_RASPBERRY = False
if is_raspberry():
    IS_RASPBERRY = True
    import RPi.GPIO as GPIO


class OnOffButton:
    def __init__(self, stop_event: Event, thread_stopped_counter: ThreadSafeInt, amount_stop_threads_names: ThreadSafeList = None):
        self._stop_event = stop_event
        self.thread_stopped_counter: ThreadSafeInt = thread_stopped_counter
        self.amount_stop_threads_names: ThreadSafeList = amount_stop_threads_names
        self.active_pin: int = 0
        self.att_comm_pin: int = 0
        if IS_RASPBERRY:
            # self.raspberry: Raspberry = Raspberry()
            # self.load_settings()
            # self.activate_pins()
            pass

        print("ON/OFF Button active")

    def load_settings(self):
        with open(get_project_root() / 'data/settings.json') as f:
            settings = json.load(f)
        # self.active_pin = settings["on_off_button"]["active_pin"]
        self.att_comm_pin = settings["on_off_button"]["att_comm_pin"]

    def activate_pins(self):
        print ("Starting...\n")
        GPIO.cleanup()
        time.sleep(1)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.att_comm_pin, GPIO.OUT)
        GPIO.output(self.att_comm_pin, GPIO.HIGH)
        time.sleep(1)

        GPIO.setup(self.att_comm_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    def set_active_pin(self, state: bool):
        if isinstance(self.active_pin, list):
            for pin in self.active_pin:
                GPIO.setup(pin, GPIO.OUT)
                if state:
                    GPIO.output(pin, GPIO.LOW)
                else:
                    GPIO.output(pin, GPIO.HIGH)
        else:
            GPIO.setup(self.active_pin, GPIO.OUT)
            if state:
                GPIO.output(self.active_pin, GPIO.LOW)
            else:
                GPIO.output(self.active_pin, GPIO.HIGH)
    
    def shutdown(self):
        os.system("sudo shutdown now")

    def run(self):
        return
        if IS_RASPBERRY:
            PIN = 15

            print ("Starting...\n")
            GPIO.cleanup()
            time.sleep(1)

            GPIO.setup(PIN, GPIO.OUT)
            GPIO.output(PIN, GPIO.HIGH)
            time.sleep(1)

            GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

            while True:
                start = time.time()
                while (not GPIO.input(PIN)):
                    time.sleep(0.01)

                if time.time() - start < 0.1:
                    GPIO.setup(PIN, GPIO.OUT, initial=0)
                    time.sleep(0.05)
                    GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                else:
                    print("Shutdown request detected\n")

                    # Acknowledge by setting the GPIO pin as Output, Low
                    GPIO.setup(PIN, GPIO.OUT)
                    GPIO.output(PIN, GPIO.LOW)
                    time.sleep(0.01)
                    GPIO.output(PIN, GPIO.HIGH)
                    GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                    self.shutdown()

                                
        self.thread_stopped_counter.increment()
        self.amount_stop_threads_names.delete(self.__class__.__name__)
        print("ON/OFF Button stopped")


if __name__ == "__main__":
    try:
        GPIO.setmode(GPIO.BCM)
        off_event = Event()
        on_off_button = OnOffButton(off_event, ThreadSafeInt())
        on_off_button.run()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        off_event.set()
        GPIO.cleanup()

