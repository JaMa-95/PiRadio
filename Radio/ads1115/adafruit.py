import time, board, busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


class AdsObject:

    def __init__(self, pin):
        i2c = busio.I2C(board.SCL, board.SDA) # Create the I2C bus
        ads = ADS.ADS1115(i2c) # Create the ADC object using the I2C bus
        if pin == 1:
            self.chan = AnalogIn(ads, ADS.P1) # Create single-ended input on channel 0
        elif pin == 2:
            self.chan = AnalogIn(ads, ADS.P2)  # Create single-ended input on channel 0
        elif pin == 3:
            self.chan = AnalogIn(ads, ADS.P3)  # Create single-ended input on channel 0
        else:
            self.chan = AnalogIn(ads, ADS.P0)  # Create single-ended input on channel 0

    def getValue(self):
        return self.chan.value

    def getVoltage(self):
        return self.chan.voltage

    def getValueSmoothed(self):
        values = []
        for i in range(20):
            values.append(self.chan.value)

        valueSmoothed = 0
        for value in values:
            valueSmoothed += value

        return valueSmoothed / len(values)
