import time
from playsound import playsound
import vlc
import unittest
from radioFrequency import KurzFrequencies, LangFrequencies, MittelFrequencies, UKWFrequencies, SprFrequencies
from radio import USBReader


class TestFrequencies(unittest.TestCase):
    def test_main_frequency(self):
        usb_reader = USBReader()
        print("1")
        test_string = "buttonOnOff:1,buttonLang:1,buttonMittel:0,buttonKurz:0,buttonUKW:0,buttonSprMus:0,potiValue:0," \
                      "posLangKurzMittel:22,posUKW:0"
        usb_reader.set_test_command(test_string)
        usb_reader.run()
        time.sleep(2)
        test_string = "buttonOnOff:1,buttonLang:1,buttonMittel:0,buttonKurz:0,buttonUKW:0,buttonSprMus:0,potiValue:0," \
                      "posLangKurzMittel:150,posUKW:0"
        print("2")
        usb_reader.set_test_command(test_string)
        time.sleep(3)

    def test_play_local(self):
        playsound(r"C:/Users/Jakob/Documents/playlists/hipHop/DanielRifaterra-Amanni.mp3")
        playsound('C:/Users/Jakob/Documents/playlists/chillout/MOTZ4000HZ-GunFingers[MOTZVA04].mp3')

    def test_radio_frequencies_kurz(self):
        non_working_url = []
        for radio_frequency in KurzFrequencies().frequencies:
            url = radio_frequency.radio_url
            instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
            player = instance.media_player_new()
            media = instance.media_new(url)
            media.get_mrl()
            player.set_media(media)
            player.play()
            counter = 0
            is_playing = player.is_playing()
            while not is_playing:
                is_playing = player.is_playing()
                time.sleep(1)
                counter += 1
                if counter == 10:
                    non_working_url.append(radio_frequency)
                    is_playing = True
            player.stop()
        print()

    def test_radio_frequencies_lang(self):
        non_working_url = []
        for radio_frequency in LangFrequencies().frequencies:
            url = radio_frequency.radio_url
            instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
            player = instance.media_player_new()
            media = instance.media_new(url)
            media.get_mrl()
            player.set_media(media)
            player.play()
            counter = 0
            is_playing = player.is_playing()
            while not is_playing:
                is_playing = player.is_playing()
                time.sleep(1)
                counter += 1
                if counter == 10:
                    non_working_url.append(radio_frequency)
                    is_playing = True
            player.stop()
        print()

    def test_radio_frequencies_mittel(self):
        non_working_url = []
        for radio_frequency in MittelFrequencies().frequencies:
            url = radio_frequency.radio_url
            instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
            player = instance.media_player_new()
            media = instance.media_new(url)
            media.get_mrl()
            player.set_media(media)
            player.play()
            counter = 0
            is_playing = player.is_playing()
            while not is_playing:
                is_playing = player.is_playing()
                time.sleep(1)
                counter += 1
                if counter == 10:
                    non_working_url.append(radio_frequency)
                    is_playing = True
            player.stop()
        print()

    def test_radio_frequencies_ukw(self):
        non_working_url = []
        for radio_frequency in UKWFrequencies().frequencies:
            url = radio_frequency.radio_url
            instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
            player = instance.media_player_new()
            media = instance.media_new(url)
            media.get_mrl()
            player.set_media(media)
            player.play()
            counter = 0
            is_playing = player.is_playing()
            while not is_playing:
                is_playing = player.is_playing()
                time.sleep(1)
                counter += 1
                if counter == 10:
                    non_working_url.append(radio_frequency)
                    is_playing = True
            player.stop()
        print()

    def test_radio_frequencies_spr(self):
        non_working_url = []
        for radio_frequency in SprFrequencies().frequencies:
            url = radio_frequency.radio_url
            instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
            player = instance.media_player_new()
            media = instance.media_new(url)
            media.get_mrl()
            player.set_media(media)
            player.play()
            counter = 0
            is_playing = player.is_playing()
            while not is_playing:
                is_playing = player.is_playing()
                time.sleep(1)
                counter += 1
                if counter == 10:
                    non_working_url.append(radio_frequency)
                    is_playing = True
            player.stop()
        print()

    def test_single_frequencies(self):
        url = "http://stream3.polskieradio.pl:8912/;"
        instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
        player = instance.media_player_new()
        media = instance.media_new(url)
        media.get_mrl()
        player.set_media(media)
        player.audio_set_volume(20)
        player.play()
        time.sleep(10)
        player.audio_set_volume(10)
        time.sleep(4)

    def test_serial(self) -> None:
        import serial
        self.ser = serial.Serial(port='COM3', baudrate=500000)
        # compare with old usb string
        # update new values
        # update usb string
        while True:
            command_ = self.ser.read_until(b';').decode("UTF-8")
            print(command_)


if __name__ == "__main__":
    TestFrequencies().test_single_frequencies()

    # 90: http://stream.antenne1.de/90er/livestream2.mp3
# bigfm: http://audiotainment-sw.streamabc.net/atsw-bigfm-aac-128-6355201?sABC=631327q2%230%238p6297p24so0op0074r50q23325nopnr%23gjy30&aw_0_1st.playerid=twl30&amsparams=playerid:twl30;skey:1662199762
# black: http://rautemusik-de-hz-fal-stream15.radiohost.de/blackbeats?
# delta: http://regiocast.streamabc.net/rc-deltaliveshsued-mp3-192-8020733?sABC=631327ss%230%238p6297p24so0op0074r50q23325nopnr%23fgernzf.qrygnenqvb.qr&aw_0_1st.playerid=streams.deltaradio.de&amsparams=playerid:streams.deltaradio.de;skey:1662199807
# electro: http://stream.electroradio.fm/192k
# kiss: http://topradio-stream21.radiohost.de/kissfm_mp3-128?ref=internetradio&amsparams=internetradio
# paloma w: http://pool.radiopaloma.de/RADIOPALOMA.mp3
# rock w: http://s5-webradio.rockantenne.de/rockantenne
# schlaget w: http://schlager.stream.laut.fm/schlager?pl=m3u&t302=2018-07-27_15-18-07&uuid=4c44a06e-f324-4ca3-8fa5-75e8dfe968a4
# sunshine w: http://sunsl.streamabc.net/sunsl-die2000er-mp3-192-3233898?sABC=6313289p%230%238p6297p24so0op0074r50q23325nopnr%23fgernz.fhafuvar-yvir.qr&aw_0_1st.playerid=stream.sunshine-live.de&amsparams=playerid:stream.sunshine-live.de;skey:1662199964
# wdr 2: https://f111.rndfnk.com/ard/wdr/wdr2/rheinland/mp3/128/stream.mp3?cid=01FBS03TJ7KW307WSY5W0W4NYB&sid=2EFn1MfwrRYRrsMp1SSjeR5gYez&token=Tcm_ogvHY4xDc85HctPOhQqyNcQJLdpdMYomYxCkaYg&tvf=Rvd4HrllERdmMTExLnJuZGZuay5jb20
# wdr4: https://d121.rndfnk.com/ard/wdr/wdr4/live/mp3/128/stream.mp3?cid=01FBS0CPYNPWV23HTXYQE8R7AR&sid=2EFn68HE8SftThMeVKVq3vPQcln&token=rYykqGU-zIRkqJQC6ikZaZhZ9XxmbmeC0Q1V49M9bsc&tvf=FMai7MFlERdkMTIxLnJuZGZuay5jb20
# südtirol: http://139.162.156.56:8114/stream
