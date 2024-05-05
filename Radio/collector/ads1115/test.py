import time

import adafruit_ads1x15.ads1115 as ADS
import board
import busio
from adafruit_ads1x15.analog_in import AnalogIn

from statistics import mean

i2c = busio.I2C(board.SCL, board.SDA)  # Create the I2C bus
ads = ADS.ADS1115(i2c)  # Create the ADC object using the I2C bus
chan = AnalogIn(ads, ADS.P0)  # Create single-ended input on channel 0
chan1 = AnalogIn(ads, ADS.P1)  # Create single-ended input on channel 0
chan2 = AnalogIn(ads, ADS.P2)  # Create single-ended input on channel 0
chan3 = AnalogIn(ads, ADS.P3)  # Create single-ended input on channel 0

pins = [ADS.P0, ADS.P1, ADS.P2, ADS.P3]

while True:
    values = []
    for pin in pins:
        print(f"PIN: {pin}")
        chan = AnalogIn(ads, pin)
        for i in range(20):
            values.append(chan.value)
            time.sleep(0.1)
        print(f"max: {max(values)}")
        print(f"min: {min(values)}")
        print(f"mean: {mean(values)}")
        print(f"range: {max(values) - min(values)}")
        print("---------------")
        time.sleep(2)