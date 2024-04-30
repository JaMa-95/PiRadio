import json
import os
from time import sleep, time
from Radio.db.db import Database
from Radio.util.util import get_project_root
from Radio.util.RadioExceptions import SystemNotSupported
from Radio.util.util import is_raspberry
if is_raspberry():
    is_raspberry = True
    from Radio.ads1115.ads import AdsObject
    from Radio.gpio.button import RadioButtonsRaspi
else:
    is_raspberry = False


class Collector:
    def __init__(self):
        self.pin_volume = None
        self.pin_bass = None
        self.pin_treble = None
        self.pin_frequencies = None
        self.load_settings()

        if is_raspberry:
            self.buttons: RadioButtonsRaspi = RadioButtonsRaspi()
            self.ads = AdsObject(pin_frequency=self.pin_frequencies,
                                 pin_bass=self.pin_bass,
                                 pin_treble=self.pin_treble,
                                 pin_volume=self.pin_volume)
        else:
            self.ads = None
            self.buttons = None
        self.db = Database()

    def load_settings(self):
        path_settings = get_project_root() / 'data/settings.json'
        with open(path_settings.resolve()) as f:
            settings = json.load(f)
        # TODO: Loop over frequencies
        self.pin_volume = settings["volume"]["pin"]
        self.pin_bass = settings["bass"]["pin"]
        self.pin_treble = settings["treble"]["pin"]
        self.pin_frequencies = settings["frequencies"]["posLangKurzMittel"]["pin"]

    def run(self):
        if not is_raspberry:
            raise SystemNotSupported("Not a raspberry pi or unsupported version")
        while True:
            if not self.db.get_web_control_value():
                self.buttons.set_values_to_db()
                self.ads.set_to_db()
            sleep(0.0001)


if __name__ == "__main__":
    collector = Collector()
    collector.run()