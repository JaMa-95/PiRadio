from subprocess import call
from Radio.util.util import is_raspberry

if is_raspberry():
    import RPi.GPIO as GPIO


class Raspberry:
    def __init__(self):
        self.alive_pin = 16
        self.dutyCycle = 100
        self.activate_alive_pin()

        self._dutyCycleDown = True

    def activate_alive_pin(self):
        try:
            GPIO.setup(self.alive_pin, GPIO.OUT)
            self.pwm_1 = GPIO.PWM(self.alive_pin, 60)
            self.pwm_1.start(0)
        except RuntimeError:
            pass
        #self.pwm_2 = GPIO.PWM(self.alive_pin, 0.5)

    def cleanup(self):
        self.pwm_1.stop()
        GPIO.cleanup()

    @staticmethod
    def turn_raspi_off():
        print("turn off raspi")
        call("sudo shutdown -h now", shell=True)
        # call(['shutdown', '-h', 'now'], shell=False)

    def alive(self):
        self._calcDutyCycle()
        self.pwm_1.ChangeDutyCycle(self.dutyCycle)

    def _calcDutyCycle(self):
        if self._dutyCycleDown:
            self.dutyCycle -= 5
            if self.dutyCycle == 0:
                self._dutyCycleDown = False
        else:
            self.dutyCycle += 5
            if self.dutyCycle == 100:
                self._dutyCycleDown = True
        
