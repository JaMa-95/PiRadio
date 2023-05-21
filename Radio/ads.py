import datetime
import time

import adafruit_ads1x15.ads1115 as ADS
import board
import busio
from adafruit_ads1x15.analog_in import AnalogIn

from db.db import Database
from statistics import mean
from adafruit_ads1x15.ads1x15 import Mode

class AdsObject:
    def __init__(self):
        self.mittel_poti = AdsSingle(3)
        self.volume_poti = AdsSingle(2)

    def set_to_db(self):
        self.mittel_poti.set_to_db_smoothed()
        self.volume_poti.set_to_db_smoothed()


class AdsSingle:
    def __init__(self, pin):
        i2c = busio.I2C(board.SCL, board.SDA, frequency=1000000)
        # i2c = busio.I2C(board.SCL, board.SDA)  # Create the I2C bus
        self.ads = ADS.ADS1115(i2c)  # Create the ADC object using the I2C bus
        self.RATE = 860
        self.SAMPLES = 1000
        self.ads.mode = Mode.CONTINUOUS
        self.ads.data_rate = self.RATE
        self.pin = pin
        self.db = Database()

        if pin == 1:
            self.chan = AnalogIn(self.ads, ADS.P1)  # Create single-ended input on channel 0
        elif pin == 2:
            self.chan = AnalogIn(self.ads, ADS.P2)  # Create single-ended input on channel 0
        elif pin == 3:
            self.chan = AnalogIn(self.ads, ADS.P3)  # Create single-ended input on channel 0
        else:
            self.chan = AnalogIn(self.ads, ADS.P0)  # Create single-ended input on channel 0

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
        if self.pin == 2:
            num_values = 700
        else:
            num_values = 150
        for i in range(num_values):
            values.append(self.chan.value)
        middle = datetime.datetime.now()
        if self.pin == 3:
            print(max(values))
            print(min(values))
            print(f"MEAN: {mean(values)}")
            print(max(values) - min(values))

        # delete min man values
        for _ in range(10):
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

    def fast_read(self):
        _ = self.chan.value

        sample_interval = 1.0 / self.ads.data_rate

        repeats = 0
        skips = 0

        data = [None] * self.SAMPLES

        start = time.monotonic()
        time_next_sample = start + sample_interval

        # Read the same channel over and over
        for i in range(self.SAMPLES):
            # Wait for expected conversion finish time
            while time.monotonic() < (time_next_sample):
                pass

            # Read conversion value for ADC channel
            data[i] = self.chan.value

            # Loop timing
            time_last_sample = time.monotonic()
            time_next_sample = time_next_sample + sample_interval
            if time_last_sample > (time_next_sample + sample_interval):
                skips += 1
                time_next_sample = time.monotonic() + sample_interval

            # Detect repeated values due to over polling
            if data[i] == data[i - 1]:
                repeats += 1

        end = time.monotonic()
        total_time = end - start

        rate_reported = self.SAMPLES / total_time
        rate_actual = (self.SAMPLES - repeats) / total_time
        # NOTE: leave input floating to pickup some random noise
        #       This cannot estimate conversion rates higher than polling rate
        print("Took {:5.3f} s to acquire {:d} samples.".format(total_time, self.SAMPLES))
        print("")
        print("Configured:")
        print("    Requested       = {:5d}    sps".format(self.RATE))
        print("    Reported        = {:5d}    sps".format(self.ads.data_rate))
        print("")
        print("Actual:")
        print("    Polling Rate    = {:8.2f} sps".format(rate_reported))
        print("                      {:9.2%}".format(rate_reported / self.RATE))
        print("    Skipped         = {:5d}".format(skips))
        print("    Repeats         = {:5d}".format(repeats))
        print("    Conversion Rate = {:8.2f} sps   (estimated)".format(rate_actual))