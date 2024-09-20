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
            self.raspberry: Raspberry = Raspberry()
            # self.load_settings()
            self.activate_pins()

        print("ON/OFF Button active")

    def load_settings(self):
        with open(get_project_root() / 'data/settings.json') as f:
            settings = json.load(f)
        self.active_pin = settings["on_off_button"]["active_pin"]
        self.att_comm_pin = settings["on_off_button"]["att_comm_pin"]

    def activate_pins(self):
        if isinstance(self.active_pin, list):
            for idx, pin in enumerate(self.active_pin):
                if idx == 0:
                    GPIO.setup(pin, GPIO.OUT)
                    GPIO.output(pin, GPIO.HIGH)
                else:
                    GPIO.setup(pin, GPIO.IN)
        else:
            GPIO.setup(self.active_pin, GPIO.OUT)
            GPIO.output(self.active_pin, GPIO.HIGH)
        GPIO.setup(self.att_comm_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def poll(self):
        start = time.time()
        while not GPIO.input(self.att_comm_pin):
            if self._stop_event.is_set():
                break
            time.sleep(0.01)
        return time.time() - start
    

    
    def set_active_pin(self, state: bool):
        if isinstance(self.active_pin, list):
            for pin in self.active_pin:
                if state:
                    GPIO.output(pin, GPIO.LOW)
                else:
                    GPIO.output(pin, GPIO.HIGH)
        else:
            if state:
                GPIO.output(self.active_pin, GPIO.LOW)
            else:
                GPIO.output(self.active_pin, GPIO.HIGH)
    
    def shutdown(self):
        # Acknowledge by setting the GPIO pin as Output, Low
        self.set_active_pin(False)
        GPIO.setup(self.att_comm_pin, GPIO.OUT)
        GPIO.output(self.att_comm_pin, GPIO.LOW)

        time.sleep(0.01)
        # make as high again so attiny can detetct when shutdown is over -> pin low again
        GPIO.output(self.att_comm_pin, GPIO.HIGH)
        GPIO.setup(self.att_comm_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        time.sleep(0.2)
        self.set_active_pin(False)
        os.system("shutdown now -h")

    def run(self):
        if IS_RASPBERRY:
            while not self._stop_event.is_set():
                if not GPIO.wait_for_edge(self.att_comm_pin, GPIO.FALLING, timeout=3):
                    continue

                poll_duration = self.poll()
                print("Poll: ", poll_duration)
                if poll_duration < 0.1:
                    GPIO.setup(self.att_comm_pin, GPIO.OUT, initial=0)
                    time.sleep(0.05)
                    GPIO.setup(self.att_comm_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                    print("Poll ", poll_duration)
                else:
                    print("Shutdown request detected")
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

