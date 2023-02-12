import signal
import sys
import time

import RPi.GPIO as GPIO

run = False

buttons = {23: "BUT_ON", 24: "BUT_LANG", 25: "BUT_MITTEL", 12: "BUT_SPR"} # "BUT_KURZ": 8,  "BUT_UKW": 7,
def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN)

while True:
    print("---------------")
    if (GPIO.input(23) == GPIO.HIGH):
        print("Is pressed")
    else:
        print("Not pressed")
    time.sleep(1)