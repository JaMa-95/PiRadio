import time
import json
from statistics import mean
from random import randint
from typing import List
from Radio.util.util import is_raspberry
if is_raspberry():
    IS_RASPBERRY = True
    import board
    import busio
    from adafruit_ads1x15.analog_in import AnalogIn
    import adafruit_ads1x15.ads1115 as ADS
    from adafruit_ads1x15.ads1x15 import Mode
else:
    IS_RASPBERRY = False

from Radio.db.db import Database
from Radio.util.sensorMsg import AnalogData, AnalogValue
from Radio.util.util import get_project_root


class AdsObject:
    # TODO: Refactor
    def __init__(self, mock: bool = False, debug: bool = False):
        self.mock: bool = mock
        self.debug: bool = debug
        self.analog_sensors: List[AdsSingle] = []

        if not self.mock:
            i2c = busio.I2C(board.SCL, board.SDA, frequency=1000000)
                # TODO: make check for i2c device not found ValueError
            self.RATE = 860

            self.ads = ADS.ADS1115(i2c, address=0x48)  # Create the ADC object using the I2C bus
            self.ads.mode = Mode.CONTINUOUS
            self.ads.data_rate = self.RATE
        else:
            self.ads = None
        self._load_settings()



    def _load_settings(self):
        path_settings = get_project_root() / 'data/settings.json'
        with open(path_settings.resolve()) as f:
            settings = json.load(f)
        for _, analog_item in settings["analog"]["sensors"].items():
            self.analog_sensors.append(
                AdsSingle(pin=analog_item["pin"],
                          mock=self.mock,
                          address=settings["analog"]["devices"][analog_item["device"]]["address"],
                          min_=analog_item["min"],
                          max_=analog_item["max"], 
                          ads=self.ads,
                          sensivity=analog_item["sensivity"]
                          )
            )
            # self.analog_sensors.append(analog_item)

    def set_to_db(self):
        for item in self.analog_sensors:
            item.ads.set_to_db_smoothed_by_pin(item.pin, True)

    def get(self):
        data = AnalogData()
        for sensor in self.analog_sensors:
            value_ = sensor.get_value_smoothed_by_pin(sensor.pin, False)
            data.add_value(
                AnalogValue(sensor.pin, value_, sensor.min, sensor.max, sensor.sensivity)
            )
            # data.add_value(AnalogValue(item["pin"], self.ads.get_value_smoothed_by_pin(item["pin"], True)))
        return data


class AdsSingle:
    # TODO: REFACTOR. too many methods which are not used, bad naming
    def __init__(self, pin, mock: bool = False, address: int = 0x48, min_: int = 0, max_: int = 0, ads=None, sensivity: int = 1):
        self.pin = pin
        self.min: int = min_
        self.max: int = max_
        self.db = Database()
        self.sensivity = sensivity
        if not mock:
            self.ads: ADS.ADS1115 = ads

        self.mock = mock
        if self.mock:
            self.adas_pin = 0
        else:
            if pin == 1:
                self.adas_pin = ADS.P1
            elif pin == 2:
                self.adas_pin = ADS.P2
            elif pin == 3:
                self.adas_pin = ADS.P3
            else:
                self.adas_pin = ADS.P0

            

    def set_to_db_smoothed_by_pin(self, pin: int, high_precision: bool = False):
        try:
            value = self.get_value_smoothed_by_pin(pin, high_precision)
        except OSError as error:
            # TODO: Restart it
            pass
        self.db.replace_ads_pin_value(value, pin)

    def get_value(self):
        return self.chan.value

    def get_voltage(self):
        return self.chan.voltage

    def get_value_smoothed_by_pin(self, pin: int, high_precision: bool):
        if self.mock:
            return randint(0, 5000)
        values = []
        if high_precision:
            num_values = 500
        else:
            num_values = 50
        
        chan = AnalogIn(self.ads, self.adas_pin)

        for i in range(num_values):
            values.append(chan.value)
        
        #  delete min man values
        for _ in range(int(num_values / 10)):
            values.remove(max(values))
            values.remove(min(values))
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
