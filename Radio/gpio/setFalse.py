import RPi.GPIO as GPIO           # import RPi.GPIO module
GPIO.setmode(GPIO.BCM)            # choose BCM or BOARD
GPIO.setup(23, GPIO.OUT) # set a port/pin as an output
GPIO.output(23, False)       # set port/pin value to 1/GPIO.HIGH/True
print(False)