import json
from Radio.util.singleton import Singleton
from Radio.util.util import get_project_root, is_raspberry

if is_raspberry():
    IS_RASPBERRY_PI = True
    import RPi.GPIO as GPIO
else:
    IS_RASPBERRY_PI = False


class AudioSourceSwitcher(Singleton):
    def __init__(self):
        self.pin_a: int = 0
        self.pin_b: int = 0
        self.devices: list = []
        self.current_device: int = 0

        self.load_from_settings()
        self.value_a: bool = False
        self.value_b: bool = False
        if IS_RASPBERRY_PI:
            GPIO.setup(self.pin_a, GPIO.OUT)
            GPIO.output(self.pin_a, self.value_a)
            GPIO.setup(self.pin_b, GPIO.OUT)
            GPIO.output(self.pin_b, self.value_b)
        self.set_startup()

    def load_from_settings(self):
        path_settings = get_project_root() / 'data/settings.json'
        with open(path_settings.resolve()) as f:
            settings = json.load(f)
        self.pin_a = settings["audio"]["switcher"]["pin_a"]
        self.pin_b = settings["audio"]["switcher"]["pin_b"]
        self.devices = settings["audio"]["switcher"]["devices"]

    def set_startup(self):
        for device in self.devices:
            if device["startup"]:
                self.value_a = device["A"]
                self.value_b = device["B"]
                if IS_RASPBERRY_PI:
                    GPIO.output(self.pin_a, self.value_a)
                    GPIO.output(self.pin_b, self.value_b)
                break
        
    def switch(self, A: bool, B: bool):
        self.value_a = A
        self.value_b = B
        if IS_RASPBERRY_PI:
            GPIO.output(self.pin_a, self.value_a)
            GPIO.output(self.pin_b, self.value_b)

    def rotate_source(self):
        self.current_device += 1
        if self.current_device >= len(self.devices):
            self.current_device = 0
        self.value_a = self.devices[self.current_device]["A"]
        self.value_b = self.devices[self.current_device]["B"]
        print("ROTATE SOURCE: ", self.devices[self.current_device]["device"])
        if IS_RASPBERRY_PI:
            GPIO.output(self.pin_a, self.value_a)
            GPIO.output(self.pin_b, self.value_b)
        