import time

import adafruit_ads1x15.ads1115 as ADS
import board
import busio
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_ads1x15.ads1x15 import Mode

from statistics import mean

i2c = busio.I2C(board.SCL, board.SDA)  # Create the I2C bus
ads = ADS.ADS1115(i2c)  # Create the ADC object using the I2C bus
ads.data_rate = 860
ads.mode = Mode.CONTINUOUS
chan = AnalogIn(ads, ADS.P0)  # Create single-ended input on channel 0
chan1 = AnalogIn(ads, ADS.P1)  # Create single-ended input on channel 0
chan2 = AnalogIn(ads, ADS.P2)  # Create single-ended input on channel 0
chan3 = AnalogIn(ads, ADS.P3)  # Create single-ended input on channel 0

pins = [ADS.P0, ADS.P1, ADS.P2, ADS.P3]

while True:
    values = []
    num_values = 100

    start = time.time()
    for i in range(num_values):
        values.append(chan3.value)

    #  delete min man values
    for _ in range(10):
        for _ in range(int(num_values / 10)):
            values.remove(max(values))
            values.remove(min(values))
        else:
            break
    end = time.time()
    # if high_precision:
    #    time_end = time.time()
    print(f"DURATION: {end - start}")
    print(f"max: {max(values)}")
    print(f"min: {min(values)}")
    print(f"mean: {mean(values)}")
    print(f"range: {max(values) - min(values)}")
    print("---------------")