from dataclasses import dataclass
from pathlib import Path
import json

from Radio.util.util import get_project_root

min_value = 606
max_value_kurz_mittel_lang = 17150
max_value_ukw = 21100


@dataclass
class RadioFrequency:
    name: str = ""
    minimum: int = 0
    maximum: int = 0
    sweet_spot: int = 0
    radio_name: str = ""
    radio_url: str = ""

    def __init__(self, name: str = "", minimum: int = 0, maximum: int = 0, radio_name: str = "", radio_url: str = "",
                 radio_name_re: str = "", radio_url_re: str = ""):
        self.name = name
        self.minimum = minimum
        self.maximum = maximum
        self.sweet_spot = int((maximum - minimum) / 2)
        self.radio_name = radio_name
        self.radio_url = radio_url
        self.radio_url_re = radio_url_re

    def from_list(self, data: list):
        self.name = data[0]
        self.minimum = data[1]
        self.maximum = data[2]
        self.sweet_spot = int((self.maximum - self.minimum) / 2)
        self.radio_name = data[3]
        self.radio_url = data[4]
        if len(data) > 5:
            self.radio_url_re = data[5]


class Frequencies:
    def __init__(self, file_name):
        self.frequencies = []
        self.min_frequency: int = 0
        self.max_frequency: int = 0
        self.load_settings()
        self.load_from_file(get_project_root() / f"/data/{file_name}")
        self.init_min_max()

    def init_min_max(self):
        number_frequencies = len(self.frequencies)
        frequency_width = int((self.max_frequency - self.min_frequency) / number_frequencies)
        for i in range(number_frequencies):
            if i == 0:
                self.frequencies[i].minimum = self.min_frequency
            else:
                self.frequencies[i].minimum = self.frequencies[i - 1].maximum + 1

            self.frequencies[i].maximum = self.frequencies[i].minimum + frequency_width

    def load_from_file(self, path: Path = None):
        if not path:
            path = get_project_root() / "/data/freq_kurz.json"
            print(f"path: {path}")
        with open(path.resolve()) as file_handler:
            frequency_data = json.load(file_handler)
        for data in frequency_data:
            freq = RadioFrequency()
            freq.from_list(data)
            self.frequencies.append(
                freq
            )

    def load_settings(self):
        path_settings = get_project_root() / 'data/settings.json'
        with open(path_settings.resolve()) as f:
            settings = json.load(f)
        self.min_frequency = settings["frequency"]["min"]
        self.max_frequency = settings["frequency"]["max"]


class KurzFrequencies(Frequencies):
    # NOT WORKING: Berum, stockholm,Falun
    def __init__(self):
        self.frequencies = []
        self.min_frequency: int = 0
        self.max_frequency: int = 0
        self.load_settings()
        self.load_from_file(get_project_root() / "/data/freq_kurz.json")
        self.init_min_max()


class LangFrequencies(Frequencies):
    # not working: That 70s Station, 80s80s Radio, 80s80s NDW, Eurodance 90, Radio 2000, rs2 -2010er, FM Top 40
    def __init__(self):
        self.frequencies = []
        self.min_frequency: int = 0
        self.max_frequency: int = 0
        self.load_settings()
        self.load_from_file(get_project_root() / "/data/freq_lang.json")
        self.init_min_max()


class MittelFrequencies(Frequencies):
    # electro swing
    def __init__(self):
        self.frequencies = []
        self.min_frequency: int = 0
        self.max_frequency: int = 0
        self.load_settings()
        self.load_from_file(get_project_root() / "/data/freq_mittel.json")
        self.init_min_max()


class UKWFrequencies(Frequencies):
    def __init__(self):
        self.frequencies = []
        self.min_frequency: int = 0
        self.max_frequency: int = 0
        self.load_settings()
        self.load_from_file(get_project_root() / "/data/freq_ukw.json")
        self.init_min_max()


class SprFrequencies(Frequencies):
    # NOT WORKING; LA MEGA ESPANA, FM MALAGA ESPANA, RADIO ENGLAND, Hardstyle radio NL, only hit japan
    def __init__(self):
        self.frequencies = []
        self.min_frequency: int = 0
        self.max_frequency: int = 0
        self.load_settings()
        self.load_from_file(get_project_root() / "/data/freq_spr.json")
        self.init_min_max()


class TaFrequencies(Frequencies):
    # NOT WORKING; LA MEGA ESPANA, FM MALAGA ESPANA, RADIO ENGLAND, Hardstyle radio NL, only hit japan
    def __init__(self):
        self.frequencies = []
        self.min_frequency: int = 0
        self.max_frequency: int = 0
        self.load_settings()
        self.load_from_file(get_project_root() / "/data/freq_ta.json")
        self.init_min_max()


if __name__ == "__main__":
    kurz = KurzFrequencies()
    lang = LangFrequencies()
    mittel = MittelFrequencies()
    ukw = UKWFrequencies()
    print()
