#!/usr/bin/env python


import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
while True:
    GPIO.wait_for_edge(3, GPIO.FALLING)

    print(f"SHUTDOWN NOW {time.time()}")
    time.sleep(0.1)