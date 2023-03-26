from dataclasses import dataclass

min_value = 20270
max_value_kurz_mittel_lang = 21800
max_value_ukw = 21800


@dataclass
class RadioFrequency:
    name: str
    minimum: int
    maximum: int
    sweet_spot: int
    radio_name: str
    radio_url: str

    def __init__(self, name: str, minimum: int, maximum: int, radio_name: str, radio_url: str, radio_name_re: str = "",
                 radio_url_re: str = ""):
        self.name = name
        self.minimum = minimum
        self.maximum = maximum
        self.sweet_spot = (maximum - minimum) / 2
        self.radio_name = radio_name
        self.radio_url = radio_url
        self.radio_url_re = radio_url_re


class Frequencies:
    def init_min_max(self):
        number_frequencies = len(self.frequencies)
        for i in range(number_frequencies):
            if i == 0:
                self.frequencies[i].minimum = min_value
            else:
                self.frequencies[i].minimum = self.frequencies[i - 1].maximum
            self.frequencies[i].maximum = int(self.frequencies[i].minimum + (max_value_kurz_mittel_lang - min_value) / \
                                              number_frequencies)


class KurzFrequencies(Frequencies):
    # NOT WORKING: Berum, stockholm,Falun
    def __init__(self):
        self.frequencies = [
            RadioFrequency("BR-NDR", 7400, 7420, "ostseewelle",
                           "http://ostseewelle--di--nacs-ais-lgc--07--cdn.cast.addradio.de/ostseewelle/nord/mp3/high?_art=dj0yJmlwPTM3LjQuMjMyLjIwNyZpZD1pY3NjeGwtazZhc2VscGdiJnQ9MTY2MjI4NTkwMSZzPTc4NjZmMjljIzM0MWIzMWQ1YTdhNmE4MWYwOTc4MzA3ZGIwYTI3NjQ2"),
            RadioFrequency("Berum", 7436, 7, "Wattwecker", "http://stream.laut.fm/wattwerker"),
            RadioFrequency("München", 135, 270, "Energy München", "http://nrj.de/muenchen"),
            RadioFrequency("Monte Ceneri", 270, 358, "Radio 3i", "https://icecast.gruppocdt.ch/radio3i-256.mp3"),
            RadioFrequency("Freies Berlin", 358, 421, "", "https://ais-edge37-live365-dal02.cdnstream.com/a51326"),
            RadioFrequency("Stuttgart", 2981, 488, "Energy Stuttgart", "http://nrj.de/stuttgart"),
            RadioFrequency("Frankfurt", 2941, 2980, "", "http://addrad.io/4454thr"),
            # http://dispatcher.rndfnk.com/rbb/radioeins/frankfurt/mp3/mid
            RadioFrequency("Brüssel", 2870, 2940, "", "http://icecast-servers.vrtcdn.be/stubru_hiphophooray-high.mp3"),
            RadioFrequency("Rias Berlin", 2752, 2870, "The Indie Blend",
                           "http://fluxfm.streamabc.net/flx-salonflux-mp3-320-6048100?sABC=631329q8%230%23q09r7p7p61o73o2sp36o15o9p26q6329%23fgernzf.syhksz.qr&aw_0_1st.playerid=streams.fluxfm.de&amsparams=playerid:streams.fluxfm.de;skey:1662200280"),
            RadioFrequency("Östersund", 2726, 2751, "Radio Svensk",
                           "http://tx-bauerse.sharp-stream.com/http_live.php?i=svenskpop_se_mp3"),
            RadioFrequency("Athen", 2715, 2725, "Athen Free Radio", "http://stream.radiojar.com/e206r95qsp8uv"),
            RadioFrequency("Hilversum", 2700, 2714, "Radio Fantasy Rotterdam", "http://213.202.241.199:8024/stream"),
            RadioFrequency("Sottens", 2658, 2699, "Back2Noize Radio", "http://stream.back2noize.com:8000/Back2Noize"),
            RadioFrequency("Stockholm", 2564, 2657, "Stockholm Närradio", "http://live.narradio.se:8030/;stream.mp3",
                           "Galaxy FM Sweden", "https://galaxyfm.radioca.st/stream"),
            RadioFrequency("München", 2601, 2633, "Radio Gong München", "http://addrad.io/44558s5"),
            RadioFrequency("SWF", 2561, 2600, "Regenbogen 2", "https://stream.regenbogen2.de/rheinneckar/mp3-128"),
            RadioFrequency("Paris", 2522, 2560, "Hotel Radio Paris", "http://radio2.pro-fhi.net:9111/stream"),
            RadioFrequency("Mailand", 2503, 2521, "Cenralo Milano", "http://streaming.centralemilano.com/m3u"),
            RadioFrequency("Brüssel", 2475, 2502, "stubru hiphophooray high",
                           "http://icecast-servers.vrtcdn.be/stubru_hiphophooray-high.mp3"),
            RadioFrequency("Hamburg", 2436, 2474, "Tidenet", "http://streaming.tidenet.de:8000/tide-192.mp3"),
            RadioFrequency("Göteborg", 2425, 2435, "", "http://184.154.43.106:8243/stream"),
            RadioFrequency("Rias Berlin", 2407, 2424, "Berlin Bohème",
                           "http://streams.fluxfm.de/berlinboheme/mp3-320/streams.fluxfm.de/"),
            RadioFrequency("Hilversum", 2390, 2406, "Amsterdam", "http://stream.zenolive.com/cfpp8xvs6neuv"),
            # https://stream.amsterdamsmostwanted.nl/8000
            RadioFrequency("Südwestfunk", 2306, 2389, "Das Ding", "https://liveradio.swr.de/tn8jep3/dasding/"),
            RadioFrequency("Straßburg", 2272, 2305, "Radio Judaica Strasbourg",
                           "http://radiojudaicastrasbourg.ice.infomaniak.ch/radiojudaicastrasbourg-128.mp3"),
            # https://www.radioking.com/play/radio-rbs-1
            RadioFrequency("Süddeutscher Rundfunk", 2251, 2271, "SWR1", "https://liveradio.swr.de/sw282p3/swr1bw/"),
            RadioFrequency("Hörby", 2227, 2250, "Malmö", "http://n0b.radiojar.com:80/bbhah441b6quv"),
            RadioFrequency("Falun", 2156, 2226, "P4 Dalarna", "https://sverigesradio.se/topsy/direkt/223-hi.mp3"),
            RadioFrequency("Bremen", 2101, 2155, "Radio Bremen",
                           "http://icecast.radiobremen.de/rb/bremennext/live/mp3/128/stream.mp3"),
            RadioFrequency("SV Rel", 2093, 2100, "Valencia", "https://streams.radio.co/sebb274c66/listen"),
            RadioFrequency("Saarbrücken", 2065, 2092, "", "https://addrad.io/4454wbr"),
            RadioFrequency("Luxemburg", 2024, 2064, "rfm luxembourg",
                           "https://www.radioking.com/play/rfm-luxembourg/137599"),
            RadioFrequency("SV Rel", 1987, 2023, "Valencia", "http://samuel.i-radio.co:8000/djradio"),
            RadioFrequency("Südwestfunk", 1943, 1989, "Bogota", "http://162.213.121.189:8050/live"),
            RadioFrequency("WDR", 1910, 1944, "WDR2",
                           "https://wdr-wdr2-rheinland.icecastssl.wdr.de/wdr/wdr2/rheinland/mp3/128/stream.mp3"),
            RadioFrequency("Bayern", 1890, 1909, "Antenne Bayern",
                           "http://stream.antenne.de/antenne/stream/mp3?aw_0_1st.playerid=com")
        ]


class LangFrequencies(Frequencies):
    # not working: That 70s Station, 80s80s Radio, 80s80s NDW, Eurodance 90, Radio 2000, rs2 -2010er, FM Top 40
    def __init__(self):
        self.frequencies = [
            RadioFrequency('Radio 20er', 0, 100, 'Bohemia Berlin',
                           'http://streams.fluxfm.de/berlinboheme/mp3-320/streams.fluxfm.de/'),
            RadioFrequency("Oldies", 100, 200, "Golden Grooves Radio",
                           "http://eu4.fastcast4u.com/proxy/carolanr2?mp=/1"),
            RadioFrequency("20-50s", 0, 100, "Cheap Music Popular", "http://s2.voscast.com:11688/live"),
            RadioFrequency("50s", 0, 100, "Onlineradio 50s", "https://stream.0nlineradio.com/50s?ref"),
            RadioFrequency("60s", 0, 100, "Radio 60s", "http://streams.fluxfm.de/60er/mp3-320/streams.fluxfm.de/"),
            RadioFrequency("70s", 0, 100, "That 70s Channel", "http://streaming.live365.com/b68000_128mp3"),
            #RadioFrequency("70s", 0, 100, "That 70s Station", "https://radio.wanderingsheep.net:8060/70s"),
            RadioFrequency("80s", 0, 100, "80s80s Radio", "http://streams.80s80s.de/web/mp3-192/play.m3u"),
            #RadioFrequency("80s", 0, 100, "80s80s Rock", "https://streams.80s80s.de/rock/mp3-192/"),
            #RadioFrequency("80s", 0, 100, "80s80s NDW", "http://streams.80s80s.de/ndw/mp3-192/play.m3u"),
            #RadioFrequency("90s", 0, 100, "90s HITS", "http://stream.zeno.fm/etd6kax1xv8uv"),
            RadioFrequency("90s", 0, 100, "Eurodance 90 - Dance Anos 90", "http://stream.zeno.fm/pdgmg8eu8k0uv"),
            #RadioFrequency("2000s", 0, 100, "Pop 90s 2000", "http://stream.zenolive.com/vy8sr3fwr0quv"),
            RadioFrequency("2000s", 0, 100, "Radio Generation 2000s", "http://138.197.117.73:8000/airtime_128"),
            RadioFrequency("2000s", 0, 100, "Radio 2000s", "https://stream.radio2000.it/"),
            #RadioFrequency("2010s", 0, 100, "rs2 - 2010er", "https://stream.rs2.de/rs2-2010er/mp3-192/?ref"),
            RadioFrequency("2010s", 0, 100, "FFH DIE 2010ER",
                           "https://streams.ffh.de/ffhchannels/mp3/playerid:RTFFH/hq2010er.mp3"),
            #RadioFrequency("Top 40", 0, 100, "FM Top 40", "http://www.1.fm/tunestream/top40/listen.pls"),
        ]
        self.init_min_max()


class MittelFrequencies(Frequencies):
    # electro swing
    def __init__(self):
        self.frequencies = [
            RadioFrequency("Rock", 0, 100, "Rock Antenne",
                           "http://stream.rockantenne.de/rockantenne/stream/mp3?aw_0_1st.playerid=com"),  # W
            RadioFrequency("Indie", 0, 100, "Delta Radio Indie", "http://streams.deltaradio.de/delta-indie/mp3-192"),
            # W
            RadioFrequency("Oldies", 0, 100, "Stereo Oldies Radio", "http://mediajukebox.dyndns.org:88/broadwave.mp3"),
            RadioFrequency("Jazz", 0, 100, "Jazz Cafe", "http://radio.wanderingsheep.tv:8059/jazzcafe320"),
            RadioFrequency("Reggaeton", 0, 100, "NRJ Reggaeton",
                           "https://scdn.nrjaudio.fm/adwz1/fr/31023/mp3_128.mp3?origineradio"),
            RadioFrequency("Cumbia", 0, 100, "Estrella 100 cumbia sonidera",
                           "https://usa5.fastcast4u.com/proxy/onztbbyh?mp=/1"),
            RadioFrequency("HipHop", 0, 100, "HipHop Station", "http://streaming.radio.co/s97881c7e0/listen"),
            RadioFrequency("HipHop Oldies", 0, 100, "Old School that Jams", "http://computronpc.net:8000/949"),
            RadioFrequency("90s", 0, 100, "90s Hits", "http://stream.zeno.fm/etd6kax1xv8uv"),
            RadioFrequency("90er", 0, 100, "http://addrad.io/4459c2f", "http://addrad.io/4459c2f"),
            RadioFrequency("eurodance", 0, 100, "Eurodance 90", "http://eurodance90stream.ddns.net/"),
            RadioFrequency("Techno", 0, 100, "Techno FM", "http://stream.techno.fm/radio320.mp3"),
            RadioFrequency("Techno", 0, 100, "Digital Impulse", "http://orion.shoutca.st:8938/stream"),
            RadioFrequency("Techno", 0, 100, "TECHNO STYLE Radio", "http://212.108.220.119:1039/stream.mp3"),
            RadioFrequency("Electro Swing", 0, 100, "Electro Swing Revolution Radio",
                           "http://stream-23.zeno.fm/gdtbdqwzrf9uv?zs=ZpZ8h41ISO6eVCeo2JJ3uQ"),
            RadioFrequency("Trance", 0, 100, "Digital Impulse - Trance Resident Paradise",
                           "http://orion.shoutca.st:8922/stream"),
            RadioFrequency("House", 0, 100, "0nlineradio HOUSE", "https://stream.0nlineradio.com/house?ref"),
            RadioFrequency("Hardstyle", 0, 100, "NRJ Hardstyle",
                           "https://scdn.nrjaudio.fm/adwz1/fr/56708/mp3_128.mp3?origineradio"),
            RadioFrequency("Drum and Base", 0, 100, "Vanilla Drum and Bass", "http://vanilladnb.co.ua:8000/stream"),
            RadioFrequency("Schlager", 0, 100, "0nlineradio Schlager Evergreens",
                           "https://stream.0nlineradio.com/schlager-evergreens?ref"),
            RadioFrequency("Blasmusik", 0, 100, "Alles Blasmusik", "http://stream.bayerwaldradio.com/allesblasmusik"),
            RadioFrequency("Klassik", 0, 100, "0nlineradio Klassik", "https://stream.0nlineradio.com/klassik?ref"),
        ]
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
    mittel = MittelFrequencies()
    print()
