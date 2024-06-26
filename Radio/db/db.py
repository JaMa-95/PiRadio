import threading
from typing import Dict

from Radio.dataProcessing.equalizerData import Equalizer
from Radio.dataProcessing.radioFrequency import RadioFrequency, Frequencies
from Radio.util.singleton import Singleton



# TODO: do i need to return copies only?
class Database(Singleton):
    def __init__(self):
        if self._Singleton__initialized:
            return
        self._Singleton__initialized = True

        self.lock = threading.Lock()

        self.web_control_value: bool = False
        self.analog_values: dict = {}
        self.button_data: dict = {}
        self.volume: int = 0
        self.radio_frequency: RadioFrequency = RadioFrequency()
        self.active_url: str = ""
        self.equalizer: Equalizer = Equalizer()

        self.shutdown: bool = False
        self.re_active: bool = False

        self.frequency_values: Dict[str, int] = {}

    ###################################################################################
    def replace_active_radio_url(self, url: str):
        with self.lock:
            self.active_url = url

    def replace_web_control_value(self, value: bool):
        with self.lock:
            self.web_control_value = value

    def replace_ads_pin_value(self, value: float, pin: int):
        with self.lock:
            self.analog_values[pin] = value

    def replace_radio_frequency(self, value: RadioFrequency):
        with self.lock:
            self.radio_frequency = value

    def replace_re_active(self, value: bool):
        with self.lock:
            self.re_active = value

    def replace_button_data(self, name: str, value):
        with self.lock:
            self.button_data[name] = value

    def replace_volume(self, value: int):
        with self.lock:
            self.volume = value

    def replace_equalizer(self, equalizer: Equalizer):
        with self.lock:
            self.equalizer = equalizer

    def replace_frequency_value(self, name: str, value: int):
        self.frequency_values[name] = value

    def replace_shutdown(self, value: bool):
        with self.lock:
            self.shutdown = value

    #######################################################################

    def get_equalizer(self) -> Equalizer:
        with self.lock:
            return self.equalizer

    def get_frequency_value(self, name) -> int | None:
        with self.lock:
            try:
                return self.frequency_values[name]
            except KeyError:
                return None

    def get_frequency_values(self) -> dict:
        with self.lock:
            return self.frequency_values

    def get_web_control_value(self):
        with self.lock:
            return self.web_control_value

    def get_ads_pin_value(self, pin: int):
        with self.lock:
            return self.analog_values[pin]

    def get_radio_frequency(self) -> RadioFrequency:
        with self.lock:
            return self.radio_frequency

    def get_re_active(self):
        with self.lock:
            return self.re_active

    def get_button_data(self, name: str):
        with self.lock:
            try:
                return self.button_data[name]
            except KeyError:
                print(f"KeyError for {name} in db buttons")
                return None
            
    def get_buttons_data(self):
        with self.lock:
            return self.button_data

    def get_volume(self):
        with self.lock:
            return self.volume

    def get_shutdown(self):
        with self.lock:
            return self.shutdown


if __name__ == "__main__":
    a = Database()
    b = Database()
    if a == b:
        print("YES")
