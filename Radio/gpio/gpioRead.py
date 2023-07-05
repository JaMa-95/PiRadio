import signal
import sys
import time

import RPi.GPIO as GPIO


def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)


GPIO.cleanup()

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)

GPIO.setup(24, GPIO.OUT)

GPIO.setup(19, GPIO.OUT)

GPIO.setup(20, GPIO.OUT)

GPIO.setup(21, GPIO.OUT)

GPIO.setup(26, GPIO.OUT)

try:
    while True:
        if (GPIO.input(23) == GPIO.HIGH):
            print("Pin 23 button is pressed")
        if (GPIO.input(24) == GPIO.HIGH):
            print("Pin 24 button is pressed")
        if (GPIO.input(19) == GPIO.HIGH):
            print("Pin 19 button is pressed")
        if (GPIO.input(20) == GPIO.HIGH):
            print("Pin 20 button is pressed")
        if (GPIO.input(21) == GPIO.HIGH):
            print("Pin 21 button is pressed")
        if (GPIO.input(26) == GPIO.HIGH):
            print("Pin 26 button is pressed")
        time.sleep(0.01)

except KeyboardInterrupt:
    print("Bye Bye")
    GPIO.cleanup()