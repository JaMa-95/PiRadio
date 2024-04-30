import time
import json
import board
import busio
from statistics import mean
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.ads1x15 import Mode

from Radio.db.db import Database
from Radio.util.util import get_project_root


class AdsObject:
    # TODO: Refactor
    def __init__(self):
        self.pin_volume: int = -1
        self.pin_bass: int = -1
        self.pin_treble: int = -1
        # TODO: multiple frequencies
        self.pin_frequency: int = -1
        self._load_settings()
        self.pins = [self.pin_frequency, self.pin_volume, self.pin_bass, self.pin_treble]

        self.ads = AdsSingle(None)

    def _load_settings(self):
        path_settings = get_project_root() / 'data/settings.json'
        with open(path_settings.resolve()) as f:
            settings = json.load(f)
        # TODO: Loop over frequencies
        self.pin_volume = settings["volume"]["pin"]
        self.pin_bass = settings["bass"]["pin"]
        self.pin_treble = settings["treble"]["pin"]
        self.pin_frequency = settings["frequencies"]["posLangKurzMittel"]["pin"]

    def set_to_db(self):
        for pin in self.pins:
            if pin == self.pin_frequency:
                self.ads.set_to_db_smoothed_by_pin(pin, True)
            else:
                self.ads.set_to_db_smoothed_by_pin(pin, True)

    def get(self):
        values = {}
        for pin in self.pins:
            values[pin] = self.ads.get_value_smoothed_by_pin(pin, True)
        return values


class AdsSingle:
    def __init__(self, pin):
        i2c = busio.I2C(board.SCL, board.SDA, frequency=1000000)
        # i2c = busio.I2C(board.SCL, board.SDA)  # Create the I2C bus
        # TODO: make check for i2c device not found ValueError
        self.ads = ADS.ADS1115(i2c)  # Create the ADC object using the I2C bus
        self.RATE = 860

        self.pin = pin
        self.db = Database()

        if self.pin == 1:
            self.chan = AnalogIn(self.ads, ADS.P1)  # Create single-ended input on channel 0
        elif self.pin == 2:
            self.chan = AnalogIn(self.ads, ADS.P2)  # Create single-ended input on channel 0
        elif self.pin == 3:
            self.chan = AnalogIn(self.ads, ADS.P3)  # Create single-ended input on channel 0
        else:
            self.chan = AnalogIn(self.ads, ADS.P0)  # Create single-ended input on channel 0

        self.ads.mode = Mode.CONTINUOUS
        self.ads.data_rate = self.RATE

    def set_to_db(self):
        value = self.get_value()
        self.db.replace_ads_pin_value(value, self.pin)

    def set_to_db_by_pin(self, pin):
        value = self.get_value()
        self.db.replace_ads_pin_value(value, pin)

    def set_to_db_smoothed(self):
        value = self.get_value_smoothed()
        self.db.replace_ads_pin_value(value, self.pin)

    def set_to_db_smoothed_by_pin(self, pin: int, high_precision: bool = False):
        try:
            value = self.get_value_smoothed_by_pin(pin, high_precision)
        except OSError as error:
            # TODO: Restart it
            pass
        # print(f"pin: {pin}, value: {value}")
        self.db.replace_ads_pin_value(value, pin)

    def get_value(self):
        return self.chan.value

    def get_voltage(self):
        return self.chan.voltage

    def get_value_smoothed(self):
        values = []
        if self.pin == 1:
            num_values = 700
            self.chan = AnalogIn(self.ads, ADS.P3)
        else:
            num_values = 150
        for i in range(num_values):
            values.append(self.chan.value)

        # delete min man values
        for _ in range(10):
            for _ in range(int(num_values / 10)):
                values.remove(max(values))
                values.remove(min(values))
            else:
                break
        if self.pin == 5:
            print(max(values) - min(values))
            print(f"MEAN: {mean(values)}")
            print(f"pin: {self.pin}")
            print("---------------")
        return mean(values)

    def get_value_smoothed_by_pin(self, pin: int, high_precision: bool):
        values = []
        if high_precision:
            num_values = 500
            # time_start = time.time()
        else:
            num_values = 100
        if pin == 1:
            self.chan = AnalogIn(self.ads, ADS.P1)  # Create single-ended input on channel 0
        elif pin == 2:
            self.chan = AnalogIn(self.ads, ADS.P2)  # Create single-ended input on channel 0
        elif pin == 3:
            self.chan = AnalogIn(self.ads, ADS.P3)  # Create single-ended input on channel 0
        else:
            self.chan = AnalogIn(self.ads, ADS.P0)  # Create single-ended input on channel 0

        for i in range(num_values):
            values.append(self.chan.value)

        #  delete min man values
        for _ in range(10):
            for _ in range(int(num_values / 10)):
                values.remove(max(values))
                values.remove(min(values))
            else:
                break
        # if high_precision:
        #    time_end = time.time()
        #    print(f"DURATION 2: {time_end - time_start}")
        return mean(values)


if __name__ == "__main__":
    ads = AdsObject(pin_frequency=1, pin_volume=2, pin_treble=0, pin_bass=3)
    while True:
        # TODO: Error all classes become same
        value = ads.frequency_poti.get_value_smoothed()
        print(value)
        value = ads.volume_poti.get_value_smoothed()
        print(value)
        value = ads.bass_poti.get_value_smoothed()
        print(value)
        value = ads.treble_poti.get_value_smoothed()
        print(value)
        time.sleep(1)
        if ads.treble_poti == ads.volume_poti:
            print("YESSSSSSSS")
