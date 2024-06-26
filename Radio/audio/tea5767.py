import json
import sys

from Radio.util.dataTransmitter import Subscriber
import subprocess
import time
from Radio.util.util import get_project_root, is_raspberry
from Radio.util.dataTransmitter import Publisher

if is_raspberry():
    import smbus as smbus


class FmModule(Subscriber):
    def __init__(self, publisher: Publisher = Publisher()):
        self.i2c_address: int = 0x60
        self.i2c: smbus.SMBus = None
        self.active: bool = True
        self.frequency = 0
        self.publisher: Publisher = publisher
        self.publisher.attach(self)

        self.frequency_value_max: int = 1
        self.frequency_value_min: int = 0
        self.load_from_settings()
        self._init_fm_module()

        self.current_fm_frequency: float = 0

        self.fm_min: int = 87.5
        self.fm_max: int = 108.0

    def _init_fm_module(self):
        if self.active:
            try:
                self.i2c = smbus.SMBus(1)
                self.i2c.write_quick(self.i2c_address)
                print("FM module initialized")
            except IOError:
                print("FM module not connected")
                self.active = False

    def load_from_settings(self):
        path_settings = get_project_root() / 'data/settings.json'
        with open(path_settings.resolve()) as f:
            settings = json.load(f)
        self.i2c_address = settings["audio"]["fm_module"]["address"]
        self.active = settings["audio"]["fm_module"]["active"]
        for _, analog in settings["analog"]["sensors"].items():
            if analog["is_frequency"]:
                print("MAX IS: ", analog["max"])
                self.frequency_value_max = analog["max"]
                self.frequency_value_min = analog["min"]

    def __del__(self):
        if self.active:
            self.i2c.close()
        print("FM module stopped")
    
    def run(self):
        while self.active:
            # update fm data 
            time.sleep(1)

    def calcuulate_fm_value(self, frequency_value: int) -> float:
        valueScaled = (frequency_value - self.frequency_value_min) / (self.frequency_value_max - self.frequency_value_min) * (self.fm_max - self.fm_min) + self.fm_min
        return valueScaled

    def update(self):
        content = self.publisher.get_content()
        if self.active:
            if "freq_fm:" in content:
                frequency_value = content.strip("freq_fm:")
                print("Frequency value: ", frequency_value)
                fm_frequency = self.calcuulate_fm_value(float(frequency_value))
                print("FM frequency: ", fm_frequency)
                self.set_freq(fm_frequency)
            elif content == "stop":
                print("MUTING FM module")
                self.mute()
            elif "volume" in content:
                self.set_volume(int(content.strip("volume:")))
            else:
                pass
                # print(f"unknown content at audio player: {content}")

    def set_volume(self, volume):
        print("Volume not supported by FM module")

    def set_freq(self, fm_frequency):
        """set Radio to specific frequency"""
        freq14bit = int(4 * (
                fm_frequency * 1000000 + 225000) / 32768)  # Frequency distribution for two bytes (according to the data sheet)
        freqH = freq14bit >> 8  #int (freq14bit / 256)
        freqL = freq14bit & 0xFF

        data = [0 for i in range(4)]  # Descriptions of individual bits in a byte - viz.  catalog sheets
        init = freqH  # freqH # 1.bajt (MUTE bit; Frequency H)  // MUTE is 0x80
        data[0] = freqL  # 2.bajt (frequency L)
        data[1] = 0xB0  #0b10110000 # 3.bajt (SUD; SSL1, SSL2; HLSI, MS, MR, ML; SWP1)
        data[2] = 0x10  #0b00010000 # 4.bajt (SWP2; STBY, BL; XTAL; smut; HCC, SNC, SI)
        data[3] = 0x00  #0b00000000 # 5.bajt (PLREFF; DTC; 0; 0; 0; 0; 0; 0)
        try:
            self.i2c.write_i2c_block_data(self.i2c_address, init, data)  # Setting a new frequency to the circuit
        except IOError:
            subprocess.call(['i2cdetect', '-y', '1'])

    def mute(self):
        """"mute radio"""
        freq14bit = int(4 * (0 * 1000000 + 225000) / 32768)
        freqL = freq14bit & 0xFF
        data = [0 for i in range(4)]
        init = 0x80
        data[0] = freqL
        data[1] = 0xB0
        data[2] = 0x10
        data[3] = 0x00
        try:
            self.i2c.write_i2c_block_data(self.i2c_address, init, data)
            print("Radio Muted")
        except IOError:
            subprocess.call(['i2cdetect', '-y', '1'])


if __name__ == '__main__':
    fm_module = FmModule()
    frequency = 101.1  # sample starting frequency
    # terminal user input infinite loop
    try:
        while True:
            print("Write command:")
            c = input()
            print(c)
            if c == 'f':  # set to 101.1
                frequency = 106.9
                fm_module.set_freq(frequency)
                time.sleep(1)
            elif c == 'v':  # set to 102.1
                frequency = 102.1
                fm_module.set_freq(frequency)
                time.sleep(1)
            elif c == 'w':  # increment by 1
                frequency += 1
                fm_module.set_freq(frequency)
                time.sleep(1)
            elif c == 's':  # decrement by 1
                frequency -= 1
                fm_module.set_freq(frequency)
                time.sleep(1)
            elif c == 'e':  # increment by 0.1
                frequency += 0.1
                fm_module.set_freq(frequency)
                time.sleep(1)
            elif c == 'd':  # decrement by 0.1
                frequency -= 0.1
                fm_module.set_freq(frequency)
                time.sleep(1)
            elif c == 'm':  # mute
                fm_module.mute()
                time.sleep(1)
            elif c == 'u':  # unmute
                fm_module.set_freq(frequency)
                time.sleep(1)
            elif c == 'q':  # exit script and cleanup
                fm_module.mute()
                break
    except KeyboardInterrupt:
        fm_module.mute()
