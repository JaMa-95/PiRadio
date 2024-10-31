import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# Setup GPIO Pins
GPIO.setup(16, GPIO.OUT)

# Set PWM instance and their frequency
pwm1 = GPIO.PWM(16, 60)
pwm1.start(0)

try:
  while True:
    for dutyCycle in range (0, 100, 5):
      pwm1.ChangeDutyCycle(dutyCycle)
      time.sleep(0.1)

    for dutyCycle in range (100, 0, -5):
      pwm1.ChangeDutyCycle(dutyCycle)
      time.sleep(0.1)

except KeyboardInterrupt:
  pwm1.stop()

# Cleans the GPIO
GPIO.cleanup()