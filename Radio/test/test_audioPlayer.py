import time
import unittest

from Radio.audioPlayer import AudioPlayer
from Radio.dataProcessor import DataProcessor
from multiprocessing import Process

from Radio.radioFrequency import RadioFrequency


class TestAudioPlayer(unittest.TestCase):
    def test_init(self):
        processor = DataProcessor()
        AudioPlayer(processor)

    def test_play_music(self):
        processor = DataProcessor()
        player = AudioPlayer(processor)

        # Could be that radio link is broken
        player.play(RadioFrequency(radio_url="https://relax.stream.publicradio.org/relax.mp3?srcid"))
        time.sleep(3)
        self.assertTrue(player.player.is_playing())

    def test_play_music_pub_sub(self):
        processor = DataProcessor()
        player = AudioPlayer(processor)

        p_send = Process(target=player.run)
        p_send.start()
        p_send.join()

        processor.publish(RadioFrequency(radio_url="https://relax.stream.publicradio.org/relax.mp3?srcid"))
        # CONFIRM MUSIC IS PLAYING
        time.sleep(10)

    def test_change_bass(self):
        processor = DataProcessor()
        player = AudioPlayer(processor)
        bass = 15

        # Could be that radio link is broken
        player.play(RadioFrequency(radio_url="https://live.hunter.fm/80s_high"))
        time.sleep(3)
        player.set_bass(bass)
        time.sleep(3)
        self.assertEqual(player.equalizer.get_amp_at_index(0), bass)