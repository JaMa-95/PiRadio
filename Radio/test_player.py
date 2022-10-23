import time
import unittest
import multiprocessing
from audioPlayer import AudioPlayer
from radioFrequency import RadioFrequency
from radio import Radio

class SimpleTest(unittest.TestCase):
    def test_player(self):
        radio = Radio()
        audio = AudioPlayer(radio)
        frequency = RadioFrequency("chillout", 0, 100, 50)
        radio.add_content(frequency)
        #radio.updateSubscribers()

        print("start")
        time.sleep(4)
        print("stop")

