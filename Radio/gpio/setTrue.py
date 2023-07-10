import time

import RPi.GPIO as GPIO           # import RPi.GPIO module

GPIO.setmode(GPIO.BCM)            # choose BCM or BOARD
GPIO.cleanup()
GPIO.setup(26, GPIO.OUT) # set a port/pin as an output
GPIO.output(26, GPIO.HIGH)       # set port/pin value to 1/GPIO.HIGH/True

GPIO.setup(20, GPIO.OUT) # set a port/pin as an output
GPIO.output(20, GPIO.HIGH)       # set port/pin value to 1/GPIO.HIGH/True

GPIO.setup(4, GPIO.OUT) # set a port/pin as an output
GPIO.output(4, True)       # set port/pin value to 1/GPIO.HIGH/True

GPIO.setup(13, GPIO.OUT, initial=0)
GPIO.output(13, True)
time.sleep(2)
GPIO.output(13, GPIO.HIGH)
time.sleep(2)
GPIO.output(13, 1)

GPIO.setup(19, GPIO.OUT)
GPIO.output(19, True)


print(True)
