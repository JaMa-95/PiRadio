import time
from dataclasses import dataclass
import json
import vlc

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
    radio_name_re: str = ""
    radio_url: str = ""
    radio_url_re: str = ""
    re_active: bool = False

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

    def from_list(self, data: list) -> bool:
        if len(data) != 8:
            if len(data) >= 0:
                raise TypeError(f"data length incorrect. Not equal 7: {len(data)}. Name: {data[0]}")
            else:
                raise TypeError(f"data length incorrect. Not equal 7: {len(data)}.")
        self.name = data[0]
        self.minimum = int(data[1])
        self.maximum = int(data[2])
        self.sweet_spot = int((self.maximum - self.minimum) / 2)
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
            self.re_active
        ]

    def test_radio_frequency(self, test_re: bool = False):
        if test_re:
            url = self.radio_url_re
        else:
                url = self.radio_url
        instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
        player = instance.media_player_new()
        media = instance.media_new(url)
        media.get_mrl()
        player.set_media(media)
        player.audio_set_volume(0)
        player.play()
        for _ in range(5):
            is_playing = player.is_playing()
            if is_playing:
                break
            else:
                time.sleep(1)
        player.stop()
        return is_playing


class Frequencies:
    def __init__(self, file_name: str = None):
        self.frequencies = []
        self.min_frequency: int = 0
        self.max_frequency: int = 0
        self.load_settings()
        if file_name:
            self.load_from_file(f"data/{file_name}")
            self.init_min_max()
        self.name: str = ""

    def test_radio_frequencies(self) -> dict:
        result = {"working": [], "broken": []}
        for frequency in self.frequencies:
            url = frequency.radio_url
            instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
            player = instance.media_player_new()
            media = instance.media_new(url)
            media.get_mrl()
            player.set_media(media)
            player.audio_set_volume(0)
            player.play()
            for _ in range(5):
                is_playing = player.is_playing()
                if is_playing:
                    break
            if is_playing == 1:
                result["working"].append(frequency)
            else:
                result["broken"].append(frequency)
            player.stop()
        return result

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
            path = 'data/freq_kurz_2.json'
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


class KurzFrequencies(Frequencies):
    # NOT WORKING: Berum, stockholm,Falun
    def __init__(self):
        self.frequencies = []
        self.min_frequency: int = 0
        self.max_frequency: int = 0
        self.load_settings()
        self.load_from_file("data/freq_kurz_2.json")
        self.init_min_max()


class LangFrequencies(Frequencies):
    # not working: That 70s Station, 80s80s Radio, 80s80s NDW, Eurodance 90, Radio 2000, rs2 -2010er, FM Top 40
    def __init__(self):
        self.frequencies = []
        self.min_frequency: int = 0
        self.max_frequency: int = 0
        self.load_settings()
        self.load_from_file("data/freq_lang.json")
        self.init_min_max()


class MittelFrequencies(Frequencies):
    # electro swing
    def __init__(self):
        self.frequencies = []
        self.min_frequency: int = 0
        self.max_frequency: int = 0
        self.load_settings()
        self.load_from_file("data/freq_mittel.json")
        self.init_min_max()


class UKWFrequencies(Frequencies):
    def __init__(self):
        self.frequencies = []
        self.min_frequency: int = 0
        self.max_frequency: int = 0
        self.load_settings()
        self.load_from_file("data/freq_ukw.json")
        self.init_min_max()


class SprFrequencies(Frequencies):
    # NOT WORKING; LA MEGA ESPANA, FM MALAGA ESPANA, RADIO ENGLAND, Hardstyle radio NL, only hit japan
    def __init__(self):
        self.frequencies = []
        self.min_frequency: int = 0
        self.max_frequency: int = 0
        self.load_settings()
        self.load_from_file("data/freq_kurz_1.json")
        self.init_min_max()


class TaFrequencies(Frequencies):
    # NOT WORKING; LA MEGA ESPANA, FM MALAGA ESPANA, RADIO ENGLAND, Hardstyle radio NL, only hit japan
    def __init__(self):
        self.frequencies = []
        self.min_frequency: int = 0
        self.max_frequency: int = 0
        self.load_settings()
        self.load_from_file("data/freq_ta.json")
        self.init_min_max()


if __name__ == "__main__":
    kurz = KurzFrequencies()
    lang = LangFrequencies()
    mittel = MittelFrequencies()
    ukw = UKWFrequencies()
    ta = TaFrequencies()
    print()
