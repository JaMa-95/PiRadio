from Radio.util import Subscriber, Singleton

"""
class DataGetter(metaclass=Subscriber):
    def __init__(self, publisher):
        self.publisher = publisher
        self.publisher.attach(self)
        self.volume = 0
        self.stream = None
        self.button_on_off = False
        self.button_lang = False
        self.button_mittel = True
        self.button_kurz = False
        self.button_ukw = False
        self.button_spr = False
        self.button_ukw = False
        self.pos_lang_mittel_kurz = 0
        self.pos_ukw_spr = 0
        self.radio_on = False

    def update(self):
        return None

    def to_dict(self):
        return {"volume": self.volume,
                "stream": self.stream,
                "button_on_off": self.button_on_off,
                "button_lang": self.button_lang,
                "button_mittel": self.button_mittel,
                "button_kurz": self.button_kurz,
                "button_ukw": self.button_ukw,
                "pos_lang_mittel_kurz": self.pos_lang_mittel_kurz,
                "pos_ukw_spr": self.pos_ukw_spr,
                "radio_on": self.radio_on}


if __name__ == "__main__":
    data_getter = DataGetter()
    data = data_getter.to_dict()
    print()
"""