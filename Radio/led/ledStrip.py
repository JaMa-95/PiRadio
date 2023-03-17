from time import sleep
from singleton import Singleton
from rpi_ws281x import PixelStrip, Color


@Singleton
class LedData:
    blink_once = False
    blink_twice = False
    fade = False
    one_after_another = False
    all_on = False
    led_on = [0, 0, 0, 0, 0, 0]
    clear = True

    def set_one_after_another_on(self):
        self.one_after_another = True
        self.clear = False

    def set_one_after_another_off(self):
        self.one_after_another = False
        self.clear = True

    def set_fade_on(self):
        self.fade = True
        self.clear = False
        self.set_led_on()

    def set_fade_off(self):
        self.fade = False
        self.clear = True
        self.set_led_off()

    def set_blink_once_on(self):
        self.blink_once = True
        self.clear = False
        self.set_led_on()

    def set_blink_once_off(self):
        self.blink_once = False
        self.clear = True
        self.set_led_off()

    def set_blink_twice_on(self):
        self.blink_once = True
        self.clear = False
        self.set_led_on()

    def set_blink_twice_off(self):
        self.blink_twice = False
        self.clear = True
        self.set_led_off()

    def set_led_on(self, led=[1, 1, 1, 1, 1]):
        self.led_on = led
        if led == [1, 1, 1, 1, 1]:
            self.all_on = True
            self.clear = False
        elif led != [0, 0, 0, 0, 0]:
            self.all_on = False
            self.clear = False
        else:
            self.all_on = False
            self.clear = True

    def set_led_off(self, led=[0, 0, 0, 0, 0]):
        self.led_on = led
        if led == [0, 0, 0, 0, 0]:
            self.all_on = False
            self.clear = True
        elif led != [0, 0, 0, 0, 0]:
            self.all_on = False
            self.clear = False
        else:
            self.all_on = True
            self.clear = False


class LedStrip:
    def __init__(self):
        self.ledData = LedData.instance()

        # LED strip configuration:
        led_count = int(18/3)  # Number of LED pixels.
        # led_pin = 12  # GPIO pin connected to the pixels (18 uses PWM!).
        led_pin = 13        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
        led_freq_hz = 800000  # LED signal frequency in hertz (usually 800khz)
        led_dma = 10  # DMA channel to use for generating signal (try 10)
        led_brightness = 255  # Set to 0 for darkest and 255 for brightest
        led_invert = False  # True to invert the signal (when using NPN transistor level shift)
        led_channel = 1  # set to '1' for GPIOs 13, 19, 41, 45 or 53

        self.strip = PixelStrip(led_count, led_pin, led_freq_hz, led_dma, led_invert, led_brightness, led_channel)
        self.strip.begin()
        self.clear()

    def run(self):
        while True:
            if self.ledData.all_on:
                print("all on")
                self.all_on()
            if self.ledData.fade:
                print("fade")
                self.fade()
            if self.ledData.blink_twice:
                print("blink twice")
                self.blink_twice()
            if self.ledData.blink_once:
                print("blink once")
                self.blink_once()
            if self.ledData.led_on != [0, 0, 0, 0, 0, 0]:
                print(f"led on: {self.ledData.led_on}")
                self.led_on()
            if self.ledData.clear:
                print("led clear")
                self.clear()
            if self.ledData.one_after_another:
                print("one after another")
                self.one_after_another()

    def led_on(self):
        for led in self.ledData.led_on:
            self.strip.setPixelColor(led, Color(255, 0, 80))
        self.strip.show()

    def blink_once(self, color=Color(255, 0, 80), length=1):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
        self.ledData.set_blink_once_on()
        self.strip.show()
        sleep(length)
        self.clear()
        self.ledData.set_blink_once_off()

    def blink_twice(self):
        self.ledData.set_blink_twice_on()
        self.blink_once()
        self.blink_once()
        self.ledData.set_blink_twice_off()

    def all_on(self):
        color = Color(255, 0, 80)
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
        self.strip.show()
        self.ledData.set_led_on()

    def fade(self, on=True, color_start=(255, 0, 80)):
        self.ledData.set_fade_on()
        if on:
            start = 100
            end = 1
            step = -1
        else:
            start = 1
            end = 100
            step = 1
        for j in range(start, end, step):
            color = Color(int(color_start[0]/j), int(color_start[1]/j), int(color_start[2]/j))
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, color)
            self.strip.show()
            sleep(0.03)
        self.ledData.set_fade_off()

    def one_after_another(self, color=Color(255, 0, 80)):
        self.ledData.set_one_after_another_on()
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
            self.strip.show()
            sleep(1)
            self.clear()
        self.ledData.set_one_after_another_off()

    def clear(self):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, Color(0, 0, 0))
        self.strip.show()
        self.ledData.set_led_off()


if __name__ == "__main__":
    ledStrip = LedStrip()
    ledStrip.fade()
    ledStrip.one_after_another()
    ledStrip.blink_twice()
    ledStrip.clear()