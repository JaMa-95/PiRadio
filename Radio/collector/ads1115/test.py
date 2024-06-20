import time

import adafruit_ads1x15.ads1115 as ADS
import board
import busio
from adafruit_ads1x15.analog_in import AnalogIn

from statistics import mean

i2c = busio.I2C(board.SCL, board.SDA)  # Create the I2C bus
ads = ADS.ADS1115(i2c)  # Create the ADC object using the I2C bus

pins = [ADS.P0, ADS.P1, ADS.P2, ADS.P3]

while True:
    values = []
    voltage = []
    for pin in pins:
        print(f"PIN: {pin}")
        chan = AnalogIn(ads, pin)
        for i in range(20):
            values.append(chan.value)
            voltage.append(chan.voltage)
            time.sleep(0.01)
        del chan
        print(f"max: {max(values)}")
        print(f"min: {min(values)}")
        print(f"mean: {mean(values)}")
        print(f"range: {max(values) - min(values)}")
        print(f"voltage: {mean(voltage)}")
        print("---------------")
        time.sleep(0.5)