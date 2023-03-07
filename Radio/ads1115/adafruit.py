import time, board, busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

i2c = busio.I2C(board.SCL, board.SDA) # Create the I2C bus

ads = ADS.ADS1115(i2c) # Create the ADC object using the I2C bus

chan = AnalogIn(ads, ADS.P3) # Create single-ended input on channel 0

print("{:>5}\t{:>5}".format('raw', 'v'))

while True:
    print("{:>5}\t{:>5.3f}".format(chan.value, chan.voltage))
    time.sleep(0.1) 