from dataclasses import dataclass
from pathlib import Path
import json

min_value = 19800
max_value_kurz_mittel_lang = 21100
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
    def __init__(self):
        self.frequencies = []

    def init_min_max(self):
        number_frequencies = len(self.frequencies)
        frequency_width = int((max_value_kurz_mittel_lang - min_value) / number_frequencies)
        for i in range(number_frequencies):
            if i == 0:
                self.frequencies[i].maximum = max_value_kurz_mittel_lang
            else:
                self.frequencies[i].maximum = self.frequencies[i - 1].minimum
            if i == 0:
                self.frequencies[i].minimum = min_value

            self.frequencies[i].minimum = self.frequencies[i].maximum - frequency_width

    def load_from_file(self, path: Path = None):
        if not path:
            path = self.get_project_root() / "Radio/data/freq_kurz.json"
        with open(path) as file_handler:
            frequency_data = json.load(file_handler)
        for data in frequency_data:
            freq = RadioFrequency()
            freq.from_list(data)
            self.frequencies.append(
                freq
            )

    @staticmethod
    def get_project_root() -> Path:
        return Path(__file__).parent.parent


class KurzFrequencies(Frequencies):
    # NOT WORKING: Berum, stockholm,Falun
    def __init__(self):
        self.frequencies = []
        self.load_from_file(self.get_project_root() / "Radio/data/freq_kurz.json")


class LangFrequencies(Frequencies):
    # not working: That 70s Station, 80s80s Radio, 80s80s NDW, Eurodance 90, Radio 2000, rs2 -2010er, FM Top 40
    def __init__(self):
        self.frequencies = []
        self.load_from_file(self.get_project_root() / "Radio/data/freq_lang.json")
        self.init_min_max()


class MittelFrequencies(Frequencies):
    # electro swing
    def __init__(self):
        self.frequencies = []
        self.load_from_file(self.get_project_root() / "Radio/data/freq_mittel.json")
        self.init_min_max()


class UKWFrequencies(Frequencies):
    def __init__(self):
        self.frequencies = [
            RadioFrequency("Relaxed", 0, 100, "1000Slots to relax", "http://hyades.shoutca.st:8714/stream"),
            RadioFrequency("Classic relax", 0, 100, "YourClassical Relax",
                           "https://relax.stream.publicradio.org/relax.mp3?srcid"),
            RadioFrequency("Chillout", 0, 100, "Relax Zone", "https://stream.radiojar.com/whwyhz188a0uv"),
            RadioFrequency("Chillout", 0, 100, "0nlineradio CHILLOUT", "https://stream.0nlineradio.com/chillout?ref"),
            # RadioFrequency("Chill", 0, 100, "Coastal de Mar Chill", "https://radio4.cdm-radio.com:18020/stream-mp3-Chill"),
            RadioFrequency("Code", 0, 100, "Techno FM", "http://stream.techno.fm/radio320.mp3"),
            RadioFrequency("Focus", 0, 100, "Music Lake - Relaxation", "http://nap.casthost.net:8626/stream"),
            # RadioFrequency("Ambient", 0, 100, "Ambient Art Sound",
            #               "https://ambientartsound.skydesignltd.com:8000/radio.mp3"),
            RadioFrequency("Ambient", 0, 100, "Ambient Sound", "http://orion.shoutca.st:8994/stream"),
            RadioFrequency("Rainy Day", 0, 100, "Sleepless Rain", "http://stream.willstare.com:8850"),
            RadioFrequency("Nature", 0, 100, "Epic Lounge - Nature Sounds",
                           "https://stream.epic-lounge.com/nature-sounds?ref"),
            RadioFrequency("Depressed", 0, 100, "Ambient Sound", "http://orion.shoutca.st:8994/stream"),
            RadioFrequency("Good vibes", 0, 100, "Ambient Sound", "http://orion.shoutca.st:8994/stream"),
            RadioFrequency("Happy", 0, 100, "Happy Hits 00", "https://streams.happyhits.co.uk/00s"),
            # RadioFrequency("Happy", 0, 100, "Positively Happy", "https://streaming.positivity.radio/pr/happy/icecast.audio"),
            RadioFrequency("Party", 0, 100, "Ambient Sound", "http://orion.shoutca.st:8994/stream"),
            # RadioFrequency("Beach", 0, 100, "Beach Party Radio", "https://ruby.torontocast.com:2995/stream"),
            # RadioFrequency("Beach", 0, 100, "Beach Vibes Radio", "https://bv.beachvibes.uk/beachvibesradio"),
            # RadioFrequency("Summer", 0, 100, "summerhitsradio", "https://jenny.torontocast.com:8024/stream"),
            # RadioFrequency("Autumn", 0, 100, "summerhitsradio", "https://jenny.torontocast.com:8024/stream"),
            # RadioFrequency("Spring", 0, 100, "summerhitsradio", "https://jenny.torontocast.com:8024/stream"),
            # RadioFrequency("Winter", 0, 100, "summerhitsradio", "https://jenny.torontocast.com:8024/stream"),
            # RadioFrequency("Celtic", 0, 100, "Techno FM", "https://jenny.torontocast.com:2000/stream/CelticMoon"),
            RadioFrequency("Cafe", 0, 100, "Epic Lounge - Coffee Bar Lounge",
                           "https://stream.epic-lounge.com/coffee-bar-lounge?ref"),
            RadioFrequency("Romantisch", 0, 100, "EPIC CLASSICAL - Classical Romance",
                           "https://stream.epic-classical.com/classical-romance?ref"),
            RadioFrequency("Dark night", 0, 100, "Techno FM", "http://stream.techno.fm/radio320.mp3"),
            RadioFrequency("Christmas Loung", 0, 100, "Epic Lounge - Christmas Lounge",
                           "https://stream.epic-lounge.com/christmas-lounge?ref"),
        ]
        self.init_min_max()


class SprFrequencies(Frequencies):
    # NOT WORKING; LA MEGA ESPANA, FM MALAGA ESPANA, RADIO ENGLAND, Hardstyle radio NL, only hit japan
    def __init__(self):
        # spanisch
        # lateinamerika
        # englisch
        # amerika
        # australien
        # französisch
        # deutsch
        # holländisch
        # italienisch
        # japanisch
        # koreanisch
        # afrikanisch
        # polnisch
        # ukraine
        self.frequencies = [
            RadioFrequency("Espana", 0, 100, "LA MEGA ESPAÑA", "https://server6.hostradios.com/8048/stream"),
            RadioFrequency("Espana", 0, 100, "FM Malaga España", "https://eu1.lhdserver.es:9035/stream"),
            RadioFrequency("Latinamerika", 0, 100, "LATIN MIX MASTERS REGGAETON RADIO",
                           "https://lmmradiocast.com/radio/8010/radio.mp3?1590197168"),
            RadioFrequency("Latinamerika", 0, 100, "LATIN MIX MASTERS RADIO",
                           "https://lmmradiocast.com/radio/8000/radio.mp3?1587013766"),
            RadioFrequency("Cumbia", 0, 100, "Cumbias De Colección", "http://stream.zenolive.com/2eq3h623km5tv"),
            RadioFrequency("Cumbia Ecuador", 0, 100, "Ecuador Cumbia", "http://us9.maindigitalstream.com:7109/stream"),
            RadioFrequency("Amerika", 0, 100, "Radio England",
                           "https://streaming02.zfast.co.uk/proxy/england?mp=/stream"),
            RadioFrequency("England", 0, 100, "Gaydio London",
                           "https://listen-gaydio.sharp-stream.com/472_gaydio_london_320_mp3"),
            RadioFrequency("England", 0, 100, "London Music Radio", "https://radiobossrelay.radioca.st/stream"),
            RadioFrequency("Australia", 0, 100, "LoveWorld Radio Australia",
                           "http://stream.radio.co/s0a970f188/listen"),
            RadioFrequency("Australia", 0, 100, "THEAUSSIEWORD Radio Australia",
                           "http://jenny.torontocast.com:8108/stream"),
            RadioFrequency("Frankreich", 0, 100, "France Bleu Normandie",
                           "http://direct.francebleu.fr/live/fbbassenormandie-midfi.mp3?ID=76zqey582k"),
            RadioFrequency("Frankreich", 0, 100, "NRJ MADE IN FRANCE",
                           "https://scdn.nrjaudio.fm/adwz1/fr/31217/mp3_128.mp3?origineradio"),
            # deutsch
            RadioFrequency("Netherlands", 0, 100, "KissFM Netherlands", "http://stream.kiss-fm.nl:9500/"),
            RadioFrequency("Netherlands", 0, 100, "Top40 Radio Netherlands", "http://s37.myradiostream.com:11662/"),
            RadioFrequency("Netherlands", 0, 100, "Hardstyle radio NL", "http://84.104.35.69:8014/hardstyle"),
            RadioFrequency("Italien", 0, 100, "Radio Rouge Italy", "http://sc10.streamingpulse.tv:8020/"),
            RadioFrequency("Italien", 0, 100, "ITALY RVRmusic", "http://radio.streemlion.com:2760/"),
            RadioFrequency("japan", 0, 100, "OnlyHit Japan", "https://j.onlyhit.us/play"),
            RadioFrequency("Korea", 0, 100, "1000Slots to relax", "http://hyades.shoutca.st:8714/stream"),
            RadioFrequency("Polen", 0, 100, "PR R Poland East", "http://c7.radioboss.fm:8261/stream"),
            RadioFrequency("Ukraine", 0, 100, "Radio Free Ukraine", "http://stream.zenolive.com/vn4r1hp339duv"),
            RadioFrequency("Ukraine", 0, 100, "Classic Radio Ukraine",
                           "https://online.classicradio.com.ua/ClassicRadio"),
            RadioFrequency("South Afrika", 0, 100, "Coastal Radio SA",
                           "http://ifastekpanel.com:1640/stream"),
            RadioFrequency("Africa", 0, 100, "UbuntuFM Radio Africa",
                           "http://stream.zenolive.com/ez10yx9e9neuv"),
        ]
        self.init_min_max()


if __name__ == "__main__":
    kurz = KurzFrequencies()
    lang = LangFrequencies()
    mittel = MittelFrequencies()
    print()
