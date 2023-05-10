import time

import adafruit_ads1x15.ads1115 as ADS
import board
import busio
from adafruit_ads1x15.analog_in import AnalogIn

from statistics import mean

i2c = busio.I2C(board.SCL, board.SDA)  # Create the I2C bus
ads = ADS.ADS1115(i2c)  # Create the ADC object using the I2C bus
chan = AnalogIn(ads, ADS.P1)  # Create single-ended input on channel 0
chan1 = AnalogIn(ads, ADS.P2)  # Create single-ended input on channel 0

while True:
    values = []
    for i in range(50):
        values.append(chan.value)
    print(max(values))
    print(min(values))
    print(mean(values))
    print(max(values) - min(values))
    print("---------------")


    time.sleep(1)