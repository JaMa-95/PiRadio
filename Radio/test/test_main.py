import time
import unittest
from threading import Thread

from Radio.dataProcessing.radioFrequency import RadioFrequency
from Radio.audio.audioPlayer import AudioPlayer
from Radio.radio import Radio, USBReader


class SimpleTest(unittest.TestCase):
    def test_main(self):
        usb_reader = USBReader()
        radio = Radio()
        audioPlayer = AudioPlayer(radio)
        print("All Subscriber: ", radio.get_subscribers())
        print("------------------------------------------------")
        test_string = "buttonOnOff:1,buttonLang:0,buttonMittel:1,buttonKurz:0,buttonUKW:0,buttonSprMus:0,potiValue:50," \
                      "posLangKurzMittel:50,posUKW:0"

        radioThread = Thread(target=radio.run)
        radioThread.start()
        usb_reader.set_test_command(test_string)
        time.sleep(5)
        print("111111111111111")
        test_string = "buttonOnOff:1,buttonLang:1,buttonMittel:0,buttonKurz:0,buttonUKW:0,buttonSprMus:0,potiValue:0," \
                      "posLangKurzMittel:22,posUKW:0"
        usb_reader.set_test_command(test_string)
        time.sleep(5)
        test_string = "buttonOnOff:1,buttonLang:0,buttonMittel:1,buttonKurz:0,buttonUKW:0,buttonSprMus:0,potiValue:0," \
                      "posLangKurzMittel:555,posUKW:0"
        print("22222222222222")
        usb_reader.set_test_command(test_string)
        time.sleep(5)
        test_string = "buttonOnOff:1,buttonLang:0,buttonMittel:1,buttonKurz:0,buttonUKW:0,buttonSprMus:0,potiValue:0," \
                      "posLangKurzMittel:50,posUKW:0"
        print("3333333333333")
        usb_reader.set_test_command(test_string)
        time.sleep(10)

    def test_main_2(self):
        audio_player = AudioPlayer(RadioFrequency("München", 0, 100, "Energy München", "http://nrj.de/muenchen"), 1)
        # audio_player.play()
        audio_player.start()
        # audio_player_thread.start()
        time.sleep(2)
        print('start')
        for i in range(100, 0, -1):
            audio_player.noise = i
            time.sleep(0.2)
        print('ende')
