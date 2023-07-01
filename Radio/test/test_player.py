import time
import unittest
import multiprocessing

from Radio.audioPlayer import AudioPlayer
from Radio.radioFrequency import RadioFrequency
from Radio.radio import Radio

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

