import time

import board
import busio
from statistics import mean
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.ads1x15 import Mode

from Radio.db.db import Database


class AdsObject:
    # TODO: Refactor
    def __init__(self, pin_frequency: int, pin_volume: int, pin_bass: int, pin_treble: int):
        self.pin_frequency = pin_frequency
        self.pin_volume = pin_volume
        self.pin_bass = pin_bass
        self.pin_treble = pin_treble
        self.pins = [pin_frequency, pin_volume, pin_bass, pin_treble]

        self.ads = AdsSingle(None)

    def set_to_db(self):
        for pin in self.pins:
            self.ads.set_to_db_smoothed_by_pin(pin)


class AdsSingle:
    def __init__(self, pin):
        i2c = busio.I2C(board.SCL, board.SDA, frequency=1000000)
        # i2c = busio.I2C(board.SCL, board.SDA)  # Create the I2C bus
        # TODO: make check for i2c device not found ValueError
        self.ads = ADS.ADS1115(i2c)  # Create the ADC object using the I2C bus
        self.RATE = 860

        self.pin = pin
        self.db = Database()

        if self.pin == 1:
            self.chan = AnalogIn(self.ads, ADS.P1)  # Create single-ended input on channel 0
        elif self.pin == 2:
            self.chan = AnalogIn(self.ads, ADS.P2)  # Create single-ended input on channel 0
        elif self.pin == 3:
            self.chan = AnalogIn(self.ads, ADS.P3)  # Create single-ended input on channel 0
        else:
            self.chan = AnalogIn(self.ads, ADS.P0)  # Create single-ended input on channel 0

        self.ads.mode = Mode.CONTINUOUS
        self.ads.data_rate = self.RATE

    def set_to_db(self):
        value = self.get_value()
        self.db.replace_ads_pin_value(value, self.pin)

    def set_to_db_by_pin(self, pin):
        value = self.get_value()
        self.db.replace_ads_pin_value(value, pin)

    def set_to_db_smoothed(self):
        value = self.get_value_smoothed()
        self.db.replace_ads_pin_value(value, self.pin)

    def set_to_db_smoothed_by_pin(self, pin):
        value = self.get_value_smoothed_by_pin(pin)
        self.db.replace_ads_pin_value(value, pin)

    def get_value(self):
        return self.chan.value

    def get_voltage(self):
        return self.chan.voltage

    def get_value_smoothed(self):
        values = []
        if self.pin == 1:
            num_values = 700
            self.chan = AnalogIn(self.ads, ADS.P3)
        else:
            num_values = 150
        for i in range(num_values):
            values.append(self.chan.value)

        # delete min man values
        for _ in range(10):
            for _ in range(int(num_values/10)):
                values.remove(max(values))
                values.remove(min(values))
            else:
                break
        if self.pin == 5:
            print(max(values) - min(values))
            print(f"MEAN: {mean(values)}")
            print(f"pin: {self.pin}")
            print("---------------")
        return mean(values)

    def get_value_smoothed_by_pin(self, pin):
        values = []
        num_values = 700
        if pin == 1:
            self.chan = AnalogIn(self.ads, ADS.P1)  # Create single-ended input on channel 0
        elif pin == 2:
            self.chan = AnalogIn(self.ads, ADS.P2)  # Create single-ended input on channel 0
        elif pin == 3:
            self.chan = AnalogIn(self.ads, ADS.P3)  # Create single-ended input on channel 0
        else:
            self.chan = AnalogIn(self.ads, ADS.P0)  # Create single-ended input on channel 0

        for i in range(num_values):
            values.append(self.chan.value)

        #  delete min man values
        for _ in range(10):
            for _ in range(int(num_values/10)):
                values.remove(max(values))
                values.remove(min(values))
            else:
                break
        return mean(values)


if __name__ == "__main__":
    ads = AdsObject(pin_frequency=1, pin_volume=2, pin_treble=0, pin_bass=3)
    while True:
        # TODO: Error all classes become same
        value = ads.frequency_poti.get_value_smoothed()
        print(value)
        value = ads.volume_poti.get_value_smoothed()
        print(value)
        value = ads.bass_poti.get_value_smoothed()
        print(value)
        value = ads.treble_poti.get_value_smoothed()
        print(value)
        time.sleep(1)
        if ads.treble_poti == ads.volume_poti:
            print("YESSSSSSSS")
