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
        self.load_from_settings()
        self.gpio_a = GPIO(self.pin_a, GPIO.OUT)
        self.value_a: bool = False
        self.gpio_a.write(self.value_a)
        self.gpio_b = GPIO(self.pin_b, GPIO.OUT)
        self.value_b: bool = False
        self.gpio_b.write(self.value_b)

    def load_from_settings(self):
        path_settings = get_project_root() / 'data/settings.json'
        with open(path_settings.resolve()) as f:
            settings = json.load(f)
        self.pin_a = settings["audio"]["switcher"]["pin_a"]
        self.pin_b = settings["audio"]["switcher"]["pin_b"]
        
    def switch(self, A: bool, B: bool):
        self.value_a = A
        self.value_b = B
        self.gpio_a.write(A)
        self.gpio_b.write(B)

    def rotate_source(self):
        if not self.value_b and not self.value_a:
            self.value_a = True
            self.gpio_a.write(self.value_a)
            return None
        elif self.value_a and self.value_b:
            self.value_a = False
            self.value_b = False
            self.gpio_a.write(self.value_a)
            self.gpio_b.write(self.value_b)
            return None
        elif self.value_a and not self.value_b:
            self.value_b = True
            self.value_a = False
            self.gpio_a.write(self.value_a)
            self.gpio_b.write(self.value_b)
            return None
        else:
            self.value_a = True
            self.value_b = True
            self.gpio_a.write(self.value_a)
            self.gpio_b.write(self.value_b)
            return None
        