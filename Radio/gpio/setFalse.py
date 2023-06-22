import RPi.GPIO as GPIO           # import RPi.GPIO module

GPIO.cleanup()

GPIO.setmode(GPIO.BCM)            # choose BCM or BOARD
GPIO.setup(17, GPIO.OUT) # set a port/pin as an output
GPIO.output(17, False)       # set port/pin value to 1/GPIO.HIGH/True
GPIO.setup(27, GPIO.OUT)
GPIO.output(27, False)
GPIO.setup(10, GPIO.OUT)
GPIO.output(10, False)
GPIO.setup(9, GPIO.OUT)
GPIO.output(9, False)

GPIO.cleanup()
print(False)
