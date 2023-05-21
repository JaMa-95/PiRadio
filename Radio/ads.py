import datetime
import time

import adafruit_ads1x15.ads1115 as ADS
import board
import busio
from adafruit_ads1x15.analog_in import AnalogIn

from db.db import Database
from statistics import mean


class AdsObject:
    def __init__(self):
        self.mittel_poti = AdsSingle(3)
        self.volume_poti = AdsSingle(2)

    def set_to_db(self):
        self.mittel_poti.set_to_db_smoothed()
        self.volume_poti.set_to_db_smoothed()


class AdsSingle:
    def __init__(self, pin):
        i2c = busio.I2C(board.SCL, board.SDA)  # Create the I2C bus
        ads = ADS.ADS1115(i2c)  # Create the ADC object using the I2C bus

        self.pin = pin
        self.db = Database()

        if pin == 1:
            self.chan = AnalogIn(ads, ADS.P1)  # Create single-ended input on channel 0
        elif pin == 2:
            self.chan = AnalogIn(ads, ADS.P2)  # Create single-ended input on channel 0
        elif pin == 3:
            self.chan = AnalogIn(ads, ADS.P3)  # Create single-ended input on channel 0
        else:
            self.chan = AnalogIn(ads, ADS.P0)  # Create single-ended input on channel 0

    def set_to_db(self):
        value = self.get_value()
        self.db.replace_ads_pin_value(value, self.pin)

    def set_to_db_smoothed(self):
        value = self.get_value_smoothed()
        self.db.replace_ads_pin_value(value, self.pin)

    def get_value(self):
        return self.chan.value

    def get_voltage(self):
        return self.chan.voltage

    def get_value_smoothed(self):
        values = []
        start = datetime.datetime.now()
        num_values = 50
        for i in range(num_values):
            values.append(self.chan.value)
        middle = datetime.datetime.now()
        if self.pin == 3:
            print(max(values))
            print(min(values))
            print(f"MEAN: {mean(values)}")
            print(max(values) - min(values))

        # delete min man values
        for _ in range(int(num_values / 4)):
            if (max(values) -min(values) > 5):
                values.remove(max(values))
                values.remove(min(values))
            else:
                break
        end = datetime.datetime.now()
        if self.pin == 3:
            print(middle - start)
            print(end - middle)
            print(max(values) - min(values))
            print(f"MEAN: {mean(values)}")
            print("---------------")
        return mean(values)
