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
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(8, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(9, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
#GPIO.setup(4, GPIO.OUT)

"""
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(20, GPIO.OUT)

GPIO.setup(21, GPIO.OUT)

GPIO.setup(26, GPIO.OUT)

#GPIO.setup(4, GPIO.OUT)

GPIO.setup(17, GPIO.OUT)

GPIO.setup(27, GPIO.OUT)

GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
"""

try:
    while True:
        if (GPIO.input(23) == GPIO.HIGH):
            print("Pin 23 button is pressed")
        if (GPIO.input(24) == GPIO.HIGH):
            print("Pin 24 button is pressed")
        if (GPIO.input(12) == GPIO.HIGH):
            print("Pin 12 button is pressed")
        if (GPIO.input(25) == GPIO.HIGH):
            print("Pin 25 button is pressed")
        if (GPIO.input(8) == GPIO.HIGH):
            print("Pin 8 button is pressed")
        if (GPIO.input(7) == GPIO.HIGH):
            print("Pin 7 button is pressed")
        if (GPIO.input(12) == GPIO.HIGH):
            print("Pin 12 button is pressed")
        if (GPIO.input(6) == GPIO.HIGH):
            print("Pin 6 button is pressed")
        if (GPIO.input(13) == GPIO.HIGH):
            print("Pin 13 button is pressed")
        else:
            print("Pin 13 button is not pressed")
        if (GPIO.input(9) == GPIO.HIGH):
            print("Pin 9 button is pressed")
        if (GPIO.input(11) == GPIO.HIGH):
            print("Pin11 button is pressed")
        #if (GPIO.input(4) == GPIO.HIGH):
        #    print("Pin 4 button is pressed")
        """
        if (GPIO.input(19) == GPIO.HIGH):
            print("Pin 19 button is pressed")
        if (GPIO.input(20) == GPIO.HIGH):
            print("Pin 20 button is pressed")
        if (GPIO.input(21) == GPIO.HIGH):
            print("Pin 21 button is pressed")
        if (GPIO.input(26) == GPIO.HIGH):
            print("Pin 26 button is pressed")
        #if (GPIO.input(4) == GPIO.HIGH):
         #   print("Pin 4 button is pressed")
        if (GPIO.input(17) == GPIO.HIGH):
            print("Pin 17 button is pressed")
        if (GPIO.input(27) == GPIO.HIGH):
            print("Pin 27 button is pressed")
        if (GPIO.input(22) == GPIO.HIGH):
            print("Pin 22 button is pressed")
        """
        time.sleep(0.01)

except KeyboardInterrupt:
    print("Bye Bye")
    GPIO.cleanup()