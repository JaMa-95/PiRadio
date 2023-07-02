import time
from time import sleep
from rpi_ws281x import PixelStrip, Color

from Radio.util.singleton import Singleton


@Singleton
class LedData:
    blink_once = False
    blink_twice = False
    fade = False
    one_after_another = False
    all_on = False
    led_on = [0, 0, 0, 0, 0, 0]
    clear = True
    radio_off = False
    raspi_off = False
    on_button_on = False
    on_button_lang = False
    on_button_mittel = False
    on_button_kurz = False
    on_button_ukw = False
    on_button_spr = False
    off_button_on = False
    off_button_lang = False
    off_button_mittel = False
    off_button_kurz = False
    off_button_ukw = False
    off_button_spr = False
    clear_now = False

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

    def set_led_on(self, led=None):
        if led is None:
            led = [1, 1, 1, 1, 1]
        self.led_on = led
        if led == [1, 1, 1, 1, 1]:
            self.all_on = True
            self.clear = False
        elif led != [0, 0, 0, 0, 0, 0]:
            self.all_on = False
            self.clear = False
        else:
            self.all_on = False
            self.clear = True

    def set_led_off(self, led=None):
        if led is None:
            led = [0, 0, 0, 0, 0, 0]
        self.led_on = led
        if led == [0, 0, 0, 0, 0, 0]:
            self.all_on = False
            self.clear = True
        elif led != [0, 0, 0, 0, 0, 0]:
            self.all_on = False
            self.clear = False
        else:
            self.all_on = True
            self.clear = False

    def set_radio_off(self):
        self.all_on = True
        self.radio_off = True
        self.clear = False

    def set_raspi_off(self):
        self.all_on = True
        self.radio_off = True
        self.clear = False

    def set_on_button_on(self):
        self.on_button_on = True
        self.off_button_on = False
        self.clear = False

    def set_off_button_on(self):
        self.on_button_on = False
        self.off_button_on = True

    def set_on_button_lang(self):
        self.on_button_lang = True
        self.off_button_lang = False
        self.clear = False

    def set_off_button_lang(self):
        self.on_button_lang = False
        self.off_button_lang = True

    def set_on_button_mittel(self):
        self.on_button_mittel = True
        self.off_button_mittel = False
        self.clear = False

    def set_off_button_mittel(self):
        self.on_button_mittel = False
        self.off_button_mittel = True

    def set_on_button_kurz(self):
        self.on_button_kurz = True
        self.off_button_kurz = False
        self.clear = False

    def set_off_button_kurz(self):
        self.on_button_kurz = False
        self.off_button_kurz = True

    def set_on_button_ukw(self):
        self.on_button_ukw = True
        self.off_button_ukw = False
        self.clear = False

    def set_off_button_ukw(self):
        self.on_button_ukw = False
        self.off_button_ukw = True

    def set_on_button_spr(self):
        self.on_button_spr = True
        self.off_button_spr = False
        self.clear = False

    def set_off_button_spr(self):
        self.off_button_spr = False
        self.off_button_spr = True

    def button_change(self, name: str, state: bool):
        # TODO: give every button its led data. Then loop over button and just turn on off led. Do this for all objects
        # which trigger led change
        pass

    def set_clear(self):
        self.all_on = False
        self.clear = True
        self.radio_off = False
        self.radio_off = False
        self.blink_once = False
        self.blink_twice = False
        self.one_after_another = False
        self.fade = False
        self.all_on = False
        self.led_on = [0, 0, 0, 0, 0, 0]


# TODO: Add queue
# TODO: intitial set buttons after first fade
class LedStrip:
    def __init__(self):
        self.ledData = LedData.instance()
        # LED strip configuration:
        led_count = int(18 / 3)  # Number of LED pixels.
        # led_pin = 12  # GPIO pin connected to the pixels (18 uses PWM!).
        led_pin = 13  # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
        led_freq_hz = 800000  # LED signal frequency in hertz (usually 800khz)
        led_dma = 10  # DMA channel to use for generating signal (try 10)
        led_brightness = 255  # Set to 0 for darkest and 255 for brightest
        led_invert = False  # True to invert the signal (when using NPN transistor level shift)
        led_channel = 1  # set to '1' for GPIOs 13, 19, 41, 45 or 53

        self.strip = PixelStrip(led_count, led_pin, led_freq_hz, led_dma, led_invert, led_brightness, led_channel)

        # self.strip.begin()
        self.clear()

    def run(self):
        while True:
            if self.ledData.on_button_on:
                self.on_button_on()
            if self.ledData.on_button_lang:
                self.on_button_lang()
            if self.ledData.on_button_mittel:
                self.on_button_mittel()
            if self.ledData.on_button_kurz:
                self.on_button_kurz()
            if self.ledData.on_button_ukw:
                self.on_button_ukw()
            if self.ledData.on_button_spr:
                self.on_button_spr()

            if self.ledData.off_button_on:
                self.off_button_on()
            if self.ledData.off_button_lang:
                self.off_button_lang()
            if self.ledData.off_button_mittel:
                self.off_button_mittel()
            if self.ledData.off_button_kurz:
                self.off_button_kurz()
            if self.ledData.off_button_ukw:
                self.off_button_ukw()
            if self.ledData.off_button_spr:
                self.off_button_spr()

            if self.ledData.raspi_off:
                self.raspi_off()
            if self.ledData.radio_off:
                self.radio_off()

            if self.ledData.all_on:
                self.all_on()
            if self.ledData.fade:
                self.fade()

            if self.ledData.blink_twice:
                self.blink_twice()
            if self.ledData.blink_once:
                self.blink_once()
            if self.ledData.one_after_another:
                self.one_after_another()

            if self.ledData.clear_now:
                self.clear()
            sleep(0.2)

    def on_button_on(self):
        # self.ledData.set_on_button_on()
        self.ledData.on_button_on = False
        self.ledData.led_on[0] = 1
        self.led_on()

    def off_button_on(self):
        # self.ledData.set_off_button_on()
        self.ledData.off_button_on = False
        self.ledData.led_on[0] = 0
        self.led_on()

    def on_button_lang(self):
        # self.ledData.set_on_button_lang()
        self.ledData.on_button_lang = False
        self.ledData.led_on[1] = 1
        self.led_on()

    def off_button_lang(self):
        # .ledData.set_off_button_lang()
        self.ledData.off_button_lang = False
        self.ledData.led_on[1] = 0
        self.led_on()

    def on_button_mittel(self):
        # self.ledData.set_on_button_mittel()
        self.ledData.on_button_mittel = False
        self.ledData.led_on[2] = 1
        self.led_on()

    def off_button_mittel(self):
        # self.ledData.set_off_button_mittel()
        self.ledData.off_button_mittel = False
        self.ledData.led_on[2] = 0
        self.led_on()

    def on_button_kurz(self):
        # self.ledData.set_on_button_kurz()
        self.ledData.on_button_kurz = False
        self.ledData.led_on[3] = 1
        self.led_on()

    def off_button_kurz(self):
        # self.ledData.set_off_button_kurz()
        self.ledData.off_button_kurz = False
        self.ledData.led_on[3] = 0
        self.led_on()

    def on_button_ukw(self):
        # self.ledData.set_on_button_ukw()
        self.ledData.on_button_ukw = False
        self.ledData.led_on[4] = 1
        self.led_on()

    def off_button_ukw(self):
        # self.ledData.set_off_button_ukw()
        self.ledData.off_button_ukw = False
        self.ledData.led_on[4] = 0
        self.led_on()

    def on_button_spr(self):
        # self.ledData.set_on_button_spr()
        self.ledData.on_button_spr = False
        self.ledData.led_on[5] = 1
        self.led_on()

    def off_button_spr(self):
        # self.ledData.set_off_button_spr()
        self.ledData.off_button_spr = False
        self.ledData.led_on[5] = 0
        self.led_on()

    def raspi_off(self):
        self.ledData.set_raspi_off()
        self.blink_once(Color(255, 0, 0))
        self.blink_once(Color(0, 255, 0))
        self.blink_once(Color(0, 0, 255))
        self.ledData.set_clear()

    def radio_off(self):
        self.ledData.set_radio_off()
        self.blink_one_color(255, 255, 255)
        self.ledData.set_clear()

    def led_on(self):
        for led, on in enumerate(reversed(self.ledData.led_on)):
            if on == 1:
                self.strip.setPixelColor(led + 1, Color(255, 0, 80))
            else:
                self.strip.setPixelColor(led + 1, Color(0, 0, 0))
        self.strip.show()

    def blink_once(self, color=Color(255, 0, 80), length=1):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
        self.ledData.set_blink_once_on()
        self.strip.show()
        sleep(length)
        self.clear()
        self.ledData.set_blink_once_off()

    def blink_twice(self, color=Color(255, 0, 80)):
        self.ledData.set_blink_twice_on()
        self.blink_once(color)
        self.blink_once(color)
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
            color = Color(int(color_start[0] / j), int(color_start[1] / j), int(color_start[2] / j))
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, color)
            self.strip.show()
            sleep(0.03)
        self.clear()
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
        self.ledData.set_clear()

    def blink_one_color(self, param, param1, param2):
        pass


if __name__ == "__main__":
    ledStrip = LedStrip()
    ledStrip.fade()
    ledStrip.one_after_another()
    ledStrip.blink_twice()
    ledStrip.clear()
