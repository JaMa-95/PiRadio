from time import sleep
from rpi_ws281x import PixelStrip, Color

class LedStrip:
    def __init__(self):
        # LED strip configuration:
        LED_COUNT = int(18/3)  # Number of LED pixels.
        #LED_PIN = 12  # GPIO pin connected to the pixels (18 uses PWM!).
        LED_PIN = 13        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
        LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
        LED_DMA = 10  # DMA channel to use for generating signal (try 10)
        LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
        LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
        LED_CHANNEL = 1  # set to '1' for GPIOs 13, 19, 41, 45 or 53

        self.strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        self.strip.begin()
        self.clear()

    def blink_once(self, color=Color(255, 0, 80), length=1):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
        self.strip.show()
        sleep(length)
        self.clear()

    def blink_twice(self):
        self.blink_once()
        self.blink_once()

    def all_on(self, color=(255, 0, 80)):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
        self.strip.show()

    def fade(self, on=True, color_start=(255, 0, 80)):
        print("FADE")
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

    def one_after_another(self, color=Color(255, 0, 80)):
        print("ONE AFTER ANOTHER")
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
            self.strip.show()
            sleep(1)
            self.clear()

    def clear(self):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, Color(0, 0, 0))
        self.strip.show()