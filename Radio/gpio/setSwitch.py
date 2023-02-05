# GPIO-Bibliothek laden
import time

import RPi.GPIO as GPIO

# BCM-Nummerierung verwenden
GPIO.setmode(GPIO.BCM)

# GPIO 17 (Pin 11) als Ausgang setzen
GPIO.setup(26, GPIO.OUT)
# GPIO 17 (Pin 11) als Ausgang setzen
GPIO.setup(9, GPIO.OUT)

while True:
    print("HIGH")
    # GPIO 17 (Pin 11) auf HIGH setzen
    GPIO.output(26, True)

    # GPIO 17 (Pin 11) auf HIGH setzen
    GPIO.output(9, True)
    time.sleep(10)

    print("LOW")
    # GPIO 17 (Pin 11) auf HIGH setzen
    GPIO.output(26, False)

    # GPIO 17 (Pin 11) auf HIGH setzen
    GPIO.output(9, False)
    time.sleep(10)