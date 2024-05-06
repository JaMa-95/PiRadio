import threading

from Radio.dataProcessing.equalizerData import Equalizer
from Radio.dataProcessing.radioFrequency import RadioFrequency
from Radio.util.singleton import Singleton


class Database(Singleton):
    def __init__(self):
        if self._Singleton__initialized:
            return
        self._Singleton__initialized = True

        self.lock = threading.Lock()

        self.web_control_value: bool = False
        self.digital_values: dict = {}
        self.button_data: dict = {}
        self.volume: int = 0
        self.radio_frequency: RadioFrequency = RadioFrequency()
        self.equalizer: Equalizer = Equalizer()

        self.shutdown: bool = False
        self.re_active: bool = False

        self.frequencies: dict = {}

    ###################################################################################

    def replace_web_control_value(self, value: bool):
        with self.lock:
            self.web_control_value = value

    def replace_ads_pin_value(self, value: float, pin: int):
        with self.lock:
            self.digital_values[pin] = value

    def replace_radio_frequency(self, value: RadioFrequency):
        with self.lock:
            self.radio_frequency = value

    # TODO: implement
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

    def replace_frequency(self, name: str, value: int):
        self.frequencies[name] = value

    def replace_shutdown(self, value: bool):
        with self.lock:
            self.shutdown = value

    #######################################################################

    def get_web_control_value(self):
        with self.lock:
            return self.web_control_value

    def get_ads_pin_value(self, pin: int):
        with self.lock:
            return self.digital_values[pin]

    def get_radio_frequency(self):
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
