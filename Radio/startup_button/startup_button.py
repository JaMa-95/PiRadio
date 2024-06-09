# Shutdown Helper Script
#
# Watchdog function:
# Pi watches for a short low pulse on GPIO and responds
# with its own short low pulse.
#
# Shutdown is requested by pulling GPIO pin 4 low for 1 sec.
# The rquest is acknowledged by setting GPIO 4 as an output
# and setting it low.

import RPi.GPIO as GPIO
import time
import subprocess

PIN = 22
PIN_TXD = 5

print ("Starting...\n")

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_TXD, GPIO.OUT)
GPIO.output(PIN_TXD, GPIO.HIGH)
while True:
    GPIO.wait_for_edge(PIN, GPIO.FALLING)
    start = time.time()
    while (not GPIO.input(PIN)):
        time.sleep(0.01)

    if time.time() - start < 0.1:
        GPIO.setup(PIN, GPIO.OUT, initial=0)
        time.sleep(0.05)
        GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        print("Poll ")
        print(time.time() - start)
        print("\n")
    else:
        print("Shutdown request detected\n")

        # Acknowledge by setting the GPIO pin as Output, Low
        GPIO.setup(PIN, GPIO.OUT)   
        GPIO.output(PIN, GPIO.LOW)
        time.sleep(0.01)
        GPIO.output(PIN, GPIO.HIGH)
        GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        subprocess.call(['shutdown', '-h', 'now'], shell=False)