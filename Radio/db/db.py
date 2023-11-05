import threading

from Radio.util.singleton import Singleton


class Database(Singleton):
    def __init__(self):
        if self._Singleton__initialized:
            return
        self._Singleton__initialized = True

        self.lock = threading.Lock()
        self.web_control_value: bool = False
        self.pins: dict = {0: 0, 1: 0, 2: 0, 3: 0}
        self.volume: int = 0
        self.stream: str = "INITIALIZING"
        self.pos_lang_mittel_kurz: int = 0
        self.pos_ukw: int = 0
        self.button_ukw: int = 0
        self.button_lang: int = 0
        self.button_mittel: int = 0
        self.button_kurz: int = 0
        self.button_on_off: int = 0
        self.button_spr_mus: int = 0
        self.button_ta: int = 0
        self.radio_name: str = ""
        self.web_control_value: bool = False
        self.poti_value_web: int = 0
        self.shutdown: bool = False
        self.bass: int = 0
        self.treble: int = 0
        self._initialize()

    def _initialize(self):
        self.web_control_value: bool = False
        self.pins: dict = {0: 0, 1: 0, 2: 0, 3: 0}
        self.volume: int = 0
        self.stream: str = "INITIALIZING"
        self.stream_re: str = "INITIALIZING"
        self.pos_lang_mittel_kurz: int = 0
        self.pos_ukw: int = 0
        self.button_ukw: int = 0
        self.button_lang: int = 0
        self.button_mittel: int = 0
        self.button_kurz: int = 0
        self.button_on_off: int = 0
        self.button_spr_mus: int = 0
        self.button_ta: int = 0
        self.radio_name: str = ""
        self.radio_name_re: str = ""
        self.web_control_value: bool = False
        self.poti_value_web: int = 0
        self.shutdown: bool = False
        self.bass: int = 0
        self.treble: int = 0
        self.treble_web: int = 0
        self.bass_web: int = 0
        self.volume_web: int = 0
        self.re_active: bool = False

    def create(self):
        return

    def clear(self):
        self._initialize()

    def init(self):
        return
        self.insert_volume(0)
        self.insert_stream("INITIALIZING")
        self.insert_pos_lang_mittel_kurz(0)
        self.insert_pos_ukw(0)
        self.insert_button_ukw(0)
        self.insert_button_lang(0)
        self.insert_button_mittel(0)
        self.insert_button_kurz(0)
        self.insert_button_on_off(0)
        self.insert_button_spr_mus(0)
        self.insert_button_ta(0)
        self.insert_ads_pin_value(0, 0)
        self.insert_ads_pin_value(0, 1)
        self.insert_ads_pin_value(0, 2)
        self.insert_ads_pin_value(0, 3)
        self.insert_radio_name("---")
        self.insert_web_control_value(False)
        self.insert_poti_value_web(0)
        self.insert_shutdown(False)
        self.insert_re_active(False)
        self.insert_radio_name_re("---")
        self.insert_stream_re("INITIALIZING")

    ###################################################################################

    def replace_web_control_value(self, value: bool):
        with self.lock:
            self.web_control_value = value

    def replace_ads_pin_value(self, value: float, pin: int):
        with self.lock:
            self.pins[pin] = value

    def replace_radio_name(self, value: str):
        with self.lock:
            self.radio_name = value

    def replace_stream(self, value: str):
        with self.lock:
            self.stream = value

    def replace_stream_re(self, value: str):
        with self.lock:
            self.stream_re = value

    def replace_radio_name_re(self, value: str):
        with self.lock:
            self.radio_name_re = value

    def replace_re_active(self, value: bool):
        with self.lock:
            self.re_active = value

    def replace_button(self, name: str, value: int):
        with self.lock:
            if name == "buttonOnOff":
                self.button_on_off = value
            elif name == "buttonTa":
                self.button_ta = value
            elif name == "buttonLang":
                self.button_lang = value
            elif name == "buttonMittel":
                self.button_mittel = value
            elif name == "buttonKurz":
                self.button_kurz = value
            elif name == "buttonUKW":
                self.button_ukw = value
            elif name == "buttonSprMus":
                self.button_spr_mus = value

    def replace_button_on_off(self, value: int):
        with self.lock:
            self.button_on_off = value

    def replace_button_ta(self, value: int):
        with self.lock:
            self.button_ta = value

    def replace_button_lang(self, value: int):
        with self.lock:
            self.button_lang = value

    def replace_button_mittel(self, value: int):
        with self.lock:
            self.button_mittel = value

    def replace_button_kurz(self, value: int):
        with self.lock:
            self.button_kurz = value

    def replace_button_ukw(self, value: int):
        with self.lock:
            self.button_ukw = value

    def replace_button_spr_mus(self, value: int):
        with self.lock:
            self.button_spr_mus = value

    def replace_volume(self, value: int):
        with self.lock:
            self.volume = value

    def replace_bass(self, value: int):
        with self.lock:
            self.bass = value

    def replace_treble(self, value: int):
        with self.lock:
            self.treble = value

    def replace_pos_lang_mittel_kurz(self, value: int):
        with self.lock:
            self.pos_lang_mittel_kurz = value

    def replace_pos_ukw(self, value: int):
        with self.lock:
            self.pos_ukw = value

    def replace_poti_value_web(self, value: int):
        with self.lock:
            self.poti_value_web = value

    def replace_shutdown(self, value: bool):
        with self.lock:
            self.shutdown = value

    #########################################################################################

    def insert_web_control_value(self, value: bool):
        with self.lock:
            self.web_control_value = value

    def insert_ads_pin_value(self, value: float, pin: int):
        with self.lock:
            self.pins[pin] = value

    def insert_radio_name(self, value: str):
        with self.lock:
            self.radio_name = value

    def insert_stream(self, value: str):
        with self.lock:
            self.stream = value

    def insert_radio_name_re(self, value: str):
        with self.lock:
            self.radio_name_re = value

    def insert_stream_re(self, value: str):
        with self.lock:
            self.stream_re = value

    def insert_re_active(self, value: bool):
        with self.lock:
            self.re_active = value

    def insert_button_on_off(self, value: int):
        with self.lock:
            self.button_on_off = value

    def insert_button_ta(self, value: int):
        with self.lock:
            self.button_ta = value

    def insert_button_lang(self, value: int):
        with self.lock:
            self.button_lang = value

    def insert_button_mittel(self, value: int):
        with self.lock:
            self.button_mittel = value

    def insert_button_kurz(self, value: int):
        with self.lock:
            self.button_kurz = value

    def insert_button_ukw(self, value: int):
        with self.lock:
            self.button_ukw = value

    def insert_button_spr_mus(self, value: int):
        with self.lock:
            self.button_spr_mus = value

    def insert_volume(self, value: int):
        with self.lock:
            self.volume = value

    def insert_bass(self, value: int):
        with self.lock:
            self.bass = value

    def insert_treble(self, value: int):
        with self.lock:
            self.treble = value

    def insert_pos_lang_mittel_kurz(self, value: int):
        with self.lock:
            self.pos_lang_mittel_kurz = value

    def insert_pos_ukw(self, value: int):
        with self.lock:
            self.pos_ukw = value

    def insert_poti_value_web(self, value: int):
        with self.lock:
            self.poti_value_web = value

    def insert_shutdown(self, value: bool):
        with self.lock:
            self.shutdown = value

    #######################################################################

    def get_volume_value_web(self):
        with self.lock:
            return self.volume_web

    def get_bass_value_web(self):
        with self.lock:
            return self.bass_web

    def get_treble_value_web(self):
        with self.lock:
            return self.treble_web

    def get_web_control_value(self):
        with self.lock:
            return self.web_control_value

    def get_ads_pin_value(self, pin: int):
        with self.lock:
            return self.pins[pin]

    def get_radio_name(self):
        with self.lock:
            return self.radio_name

    def get_stream(self):
        with self.lock:
            return self.stream

    def get_radio_name_re(self):
        with self.lock:
            return self.radio_name_re

    def get_stream_re(self):
        with self.lock:
            return self.stream_re

    def get_re_active(self):
        with self.lock:
            return self.re_active

    def get_button(self, name: str):
        with self.lock:
            if name == "buttonOnOff":
                return self.button_on_off
            elif name == "buttonTa":
                return self.button_ta
            elif name == "buttonLang":
                return self.button_lang
            elif name == "buttonMittel":
                return self.button_mittel
            elif name == "buttonKurz":
                return self.button_kurz
            elif name == "buttonUKW":
                return self.button_ukw
            elif name == "buttonSprMus":
                return self.button_spr_mus

    def get_button_on_off(self):
        with self.lock:
            return self.button_on_off

    def get_button_ta(self):
        with self.lock:
            return self.button_ta

    def get_button_on_off_web(self):
        with self.lock:
            if self.button_on_off == 1:
                return "On"
            elif self.button_on_off == 0:
                return "Off"
            return "Error"

    def get_button_lang(self):
        with self.lock:
            return self.button_lang

    def get_button_lang_web(self):
        with self.lock:
            if self.button_lang == 1:
                return "Off"
            elif self.button_lang == 0:
                return "Error"
            return "On"

    def get_button_mittel(self):
        with self.lock:
            return self.button_mittel

    def get_button_mittel_web(self):
        with self.lock:
            if self.button_mittel == 1:
                return "Off"
            elif self.button_mittel == 0:
                return "Error"
            return "On"

    def get_button_kurz(self):
        with self.lock:
            return self.button_kurz

    def get_button_kurz_web(self):
        with self.lock:
            if self.button_kurz == 1:
                return "Off"
            elif self.button_kurz == 0:
                return "Error"
            return "On"

    def get_button_ukw(self):
        with self.lock:
            return self.button_ukw

    def get_button_ukw_web(self):
        with self.lock:
            if self.button_ukw == 1:
                return "Off"
            elif self.button_ukw == 0:
                return "Error"
            return "On"

    def get_button_spr_mus(self):
        with self.lock:
            return self.button_spr_mus

    def get_button_spr_mus_web(self):
        with self.lock:
            if self.button_spr_mus == 1:
                return "Off"
            elif self.button_spr_mus == 0:
                return "Error"
            return "On"

    def get_volume(self):
        with self.lock:
            return self.volume

    def get_treble(self):
        with self.lock:
            return self.treble

    def get_bass(self):
        with self.lock:
            return self.bass

    def get_pos_lang_mittel_kurz(self):
        with self.lock:
            return self.pos_lang_mittel_kurz

    def get_pos_ukw(self):
        with self.lock:
            return self.pos_ukw

    def get_shutdown(self):
        with self.lock:
            return self.shutdown


if __name__ == "__main__":
    a = Database()
    b = Database()
    if a == b:
        print("YES")
