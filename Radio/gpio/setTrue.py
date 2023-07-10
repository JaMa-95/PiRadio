import RPi.GPIO as GPIO           # import RPi.GPIO module

GPIO.setmode(GPIO.BCM)            # choose BCM or BOARD

GPIO.setup(26, GPIO.IN) # set a port/pin as an output
GPIO.output(26, GPIO.HIGH)       # set port/pin value to 1/GPIO.HIGH/True

GPIO.setup(20, GPIO.IN) # set a port/pin as an output
GPIO.output(20, GPIO.HIGH)       # set port/pin value to 1/GPIO.HIGH/True

GPIO.setup(4, GPIO.IN) # set a port/pin as an output
GPIO.output(4, True)       # set port/pin value to 1/GPIO.HIGH/True

GPIO.setup(13, GPIO.IN)
GPIO.output(13, True)

GPIO.setup(19, GPIO.IN)
GPIO.output(19, True)

GPIO.cleanup()
print(True)
