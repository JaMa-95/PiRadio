import signal
import sys
import time

import RPi.GPIO as GPIO

run = False

buttons = {23: "BUT_ON", 24: "BUT_LANG", 25: "BUT_MITTEL", 12: "BUT_SPR"} # "BUT_KURZ": 8,  "BUT_UKW": 7,
def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

for button_pin, button_name in buttons.items():
    GPIO.setmode(GPIO.BCM)  # Broadcom pin-numbering scheme
    GPIO.setup(button_pin, GPIO.IN)  # LED pin set as output
    # GPIO.setup(butPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button pin set as input w/ pull-up

while True:
    for button_pin, button_name in buttons.items():
        GPIO.setmode(GPIO.BCM)  # Broadcom pin-numbering scheme
        GPIO.setup(button_pin, GPIO.IN)  # LED pin set as output

        print(f"{button_name}: {GPIO.input(button_pin)}")
    time.sleep(1)