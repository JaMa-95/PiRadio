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

pins = [ADS.P0]

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
        print(f"max: {max(values)}")
        print(f"min: {min(values)}")
        print(f"mean: {mean(values)}")
        print(f"range: {max(values) - min(values)}")
        print(f"voltage: {mean(voltage)}")
        print("---------------")
        time.sleep(0.5)