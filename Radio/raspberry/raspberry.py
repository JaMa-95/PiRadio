from subprocess import call
from Radio.util.util import is_raspberry

if is_raspberry():
    import RPi.GPIO as GPIO


class Raspberry:
    def __init__(self):
        self.alive_pin = 16
        self.activate_alive_pin()
        self.current_alive_state = True

    def activate_alive_pin(self):
        GPIO.setup(self.alive_pin, GPIO.OUT)
        GPIO.output(self.alive_pin, True)

    @staticmethod
    def turn_raspi_off():
        print("turn off raspi")
        call("sudo shutdown -h now", shell=True)
        # call(['shutdown', '-h', 'now'], shell=False)

    def alive():
        self.current_alive_state = not self.current_alive_state 
        GPIO.output(self.alive_pin, self.current_alive_state)
