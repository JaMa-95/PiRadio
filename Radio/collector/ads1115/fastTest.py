import datetime
import time

import adafruit_ads1x15.ads1115 as ADS
import board
import busio
from adafruit_ads1x15.analog_in import AnalogIn

from statistics import mean
from adafruit_ads1x15.ads1x15 import Mode

class AdsSingle:
    def __init__(self, pin):
        i2c = busio.I2C(board.SCL, board.SDA, frequency=1000000)
        # i2c = busio.I2C(board.SCL, board.SDA)  # Create the I2C bus
        self.ads = ADS.ADS1115(i2c)  # Create the ADC object using the I2C bus
        self.RATE = 860

        self.pin = pin

        if pin == 1:
            self.chan = AnalogIn(self.ads, ADS.P1)  # Create single-ended input on channel 0
        elif pin == 2:
            self.chan = AnalogIn(self.ads, ADS.P2)  # Create single-ended input on channel 0
        elif pin == 3:
            self.chan = AnalogIn(self.ads, ADS.P3)  # Create single-ended input on channel 0
        else:
            self.chan = AnalogIn(self.ads, ADS.P0)  # Create single-ended input on channel 0

        self.ads.mode = Mode.CONTINUOUS
        self.ads.data_rate = self.RATE

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
        if self.pin == 3:
            num_values = 700
            self.chan = AnalogIn(self.ads, ADS.P3)
        else:
            num_values = 150
        for i in range(num_values):
            values.append(self.chan.value)

        # delete min man values
        for _ in range(int(num_values/10)):
            if max(values) -min(values) > 5:
                values.remove(max(values))
                values.remove(min(values))
            else:
                break
        print(max(values) - min(values))
        print(f"MEAN: {mean(values)}")
        print("---------------")
        return mean(values)

if __name__ == "__main__":
    while True:
        adsO = AdsSingle(0)
        print(adsO.get_value_smoothed())
        time.sleep(1)