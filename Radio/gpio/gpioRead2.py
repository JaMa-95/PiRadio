import signal
import sys
import time

import RPi.GPIO as GPIO

run = False

buttons = {23: "BUT_ON", 24: "BUT_LANG", 25: "BUT_MITTEL", 12: "BUT_SPR"} # "BUT_KURZ": 8,  "BUT_UKW": 7,
def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(9, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(8, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
while True:
    if (GPIO.input(23) == GPIO.HIGH):
        print("Pin 23 button is pressed")
    if (GPIO.input(24) == GPIO.HIGH):
        print("Pin 24 button is pressed")
    if (GPIO.input(25) == GPIO.HIGH):
        print("Pin 25 button is pressed")
    if (GPIO.input(12) == GPIO.HIGH):
        print("Pin 12 button is pressed")
    if (GPIO.input(9) == GPIO.HIGH):
        print("Pin 9 button is pressed")
    if (GPIO.input(11) == GPIO.HIGH):
        print("Pin 11 button is pressed")
    if (GPIO.input(26) == GPIO.HIGH):
        print("Pin 26 button is pressed")
    if (GPIO.input(7) == GPIO.HIGH):
        print("Pin 7 button is pressed")
    if (GPIO.input(8) == GPIO.HIGH):
        print("Pin 8 is pressed")
    if (GPIO.input(13) == GPIO.HIGH):
        print("Pin 13 is pressed")
    time.sleep(1)
