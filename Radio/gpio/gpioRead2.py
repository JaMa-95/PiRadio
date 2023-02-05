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
GPIO.setup(24, GPIO.IN)
GPIO.setup(25, GPIO.IN)
GPIO.setup(12, GPIO.IN)
GPIO.setup(8, GPIO.IN)
GPIO.setup(7, GPIO.IN)

while True:
    if (GPIO.input(23) == GPIO.LOW):
        print("Pin 23 button is pressed")
    elif (GPIO.input(24) == GPIO.LOW):
        print("Pin 24 button is pressed")
    elif (GPIO.input(25) == GPIO.LOW):
        print("Pin 25 button is pressed")
    elif (GPIO.input(12) == GPIO.LOW):
        print("Pin 24 button is pressed")
    elif (GPIO.input(8) == GPIO.LOW):
        print("Pin 25 button is pressed")
    elif (GPIO.input(7) == GPIO.LOW):
        print("Pin 25 button is pressed")