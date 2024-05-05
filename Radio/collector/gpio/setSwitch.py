# GPIO-Bibliothek laden
import time

import RPi.GPIO as GPIO

# BCM-Nummerierung verwenden
GPIO.setmode(GPIO.BCM)

# GPIO 17 (Pin 11) als Ausgang setzen
GPIO.setup(4, GPIO.OUT)
# GPIO 17 (Pin 11) als Ausgang setzen
GPIO.setup(4, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(9, GPIO.OUT)

while True:
    print("HIGH")
    # GPIO 17 (Pin 11) auf HIGH setzen
    GPIO.output(4, True)
    #GPIO.output(9, True)
    #GPIO.output(17, False)
    #GPIO.output(27, False)
    time.sleep(10)

    print("LOW")
    # GPIO 17 (Pin 11) auf HIGH setzen
    GPIO.output(4, False)

    # GPIO 17 (Pin 11) auf HIGH setzen
    #GPIO.output(9, False)
    #GPIO.output(17, True)
    #GPIO.output(27, True)
    time.sleep(10)

