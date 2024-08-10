import time
from dataclasses import dataclass
import json
from typing import List

from Radio.util.util import get_project_root

min_value = 606
max_value_kurz_mittel_lang = 17150
max_value_ukw = 21100


class RadioFrequency:
    def __int__(self):
        self.name: str = ""
        self.minimum: int = 0
        self.maximum: int = 0
        self.sweet_spot: int = 0
        self.radio_name: str = ""
        self.radio_name_re: str = ""
        self.radio_url: str = ""
        self.radio_url_re: str = ""
        self.re_active: bool = False

    def __init__(self, name: str = "", minimum: int = 0, maximum: int = 0, radio_name: str = "", radio_url: str = "",
                 radio_name_re: str = "", radio_url_re: str = "", re_active: bool = False):
        self.name = name
        self.minimum = minimum
        self.maximum = maximum
        self.sweet_spot = int((maximum - minimum) / 2)
        self.radio_name = radio_name
        self.radio_name_re = radio_name_re
        self.radio_url = radio_url
        self.radio_url_re = radio_url_re
        self.re_active: bool = re_active

    def __eq__(self, other):
        if other is None:
            return False
        if self.name != other.name or \
           self.minimum != other.minimum or \
           self.maximum != other.maximum or \
           self.radio_name != other.radio_name or \
           self.radio_name_re != other.radio_name_re or \
           self.radio_url != other.radio_url or \
           self.radio_url_re != other.radio_url_re or \
           self.re_active != other.re_active:
            return False
        return True

    def copy(self):
        return RadioFrequency(
            name=self.name,
            minimum=self.minimum,
            maximum=self.maximum,
            radio_name=self.radio_name,
            radio_name_re=self.radio_name_re,
            radio_url=self.radio_url,
            radio_url_re=self.radio_url_re,
            re_active=self.re_active
        )

    def from_list(self, data: list) -> bool:
        if len(data) == 9:
            self.sweet_spot = data[8]
        elif len(data) == 8:
            self.sweet_spot = int((self.maximum - self.minimum) / 2)
        else:
            if len(data) >= 0:
                raise TypeError(f"data length incorrect. Not equal 7: {len(data)}. Name: {data[0]}")
            else:
                raise TypeError(f"data length incorrect. Not equal 7: {len(data)}.")
        self.name = data[0]
        self.minimum = int(data[1])
        self.maximum = int(data[2])

        self.radio_name = data[3]
        self.radio_url = data[4]
        self.radio_name_re = data[5]
        self.radio_url_re = data[6]
        self.re_active = data[7]
        return True

    def to_list(self) -> list:
        return [
            self.name,
            self.minimum,
            self.maximum,
            self.radio_name,
            self.radio_url,
            self.radio_name_re,
            self.radio_url_re,
            self.re_active,
            #self.sweet_spot
        ]

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "minimum": self.minimum,
            "maximum": self.maximum,
            "radio_name": self.radio_name,
            "radio_url": self.radio_url,
            "radio_name_re": self.radio_name_re,
            "radio_url_re": self.radio_url_re,
            "re_active": self.re_active,
            "sweet_spot": self.sweet_spot
        }


class Frequencies:
    def __init__(self, file_name: str = None):
        self.frequencies: List[RadioFrequency] = []
        self.min_frequency: int = 0
        self.max_frequency: int = 0
        self.load_settings()
        if file_name:
            self.load_from_file(f"data/frequencies/{file_name}")
            self.init_min_max()
        self.name: str = ""

    def init_min_max(self):
        number_frequencies = len(self.frequencies)
        frequency_width = int((self.max_frequency - self.min_frequency) / number_frequencies)
        for i in range(number_frequencies):
            if i == 0:
                self.frequencies[i].minimum = self.min_frequency
            else:
                self.frequencies[i].minimum = self.frequencies[i - 1].maximum + 1

            self.frequencies[i].maximum = self.frequencies[i].minimum + frequency_width

    def load_from_file(self, path: str = None):
        if not path:
            path = '../data/frequencies/freq_kurz_2.json'
        path = get_project_root() / path
        with open(path.resolve(), encoding='utf-8') as file_handler:
            frequency_data = json.load(file_handler)
        self.load_frequencies(frequency_data)

    def load_frequencies(self, frequency_data):
        for data in frequency_data:
            if isinstance(data, list):
                freq = RadioFrequency()
                freq.from_list(data)
                self.frequencies.append(freq)
            else:
                print(f"Loading from list with wrong data: {data}")

    def load_settings(self):
        path_settings = get_project_root() / 'data/settings.json'
        with open(path_settings.resolve()) as f:
            settings = json.load(f)
        self.min_frequency = settings["frequency"]["min"]
        self.max_frequency = settings["frequency"]["max"]

    def to_list(self) -> list:
        data = []
        for frequency in self.frequencies:
            data.append(frequency.to_list())
        return data
