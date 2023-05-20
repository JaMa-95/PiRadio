import RPi.GPIO as GPIO           # import RPi.GPIO module
GPIO.setmode(GPIO.BCM)            # choose BCM or BOARD
GPIO.setup(26, GPIO.OUT) # set a port/pin as an output
GPIO.output(26, True)       # set port/pin value to 1/GPIO.HIGH/True
GPIO.setup(4, GPIO.OUT) # set a port/pin as an output
GPIO.output(4, True)       # set port/pin value to 1/GPIO.HIGH/True
print(True)
