import time
import unittest
from multiprocessing import Process

from Radio.audio.audioPlayer import AudioPlayer
from Radio.dataProcessing.dataProcessor import DataProcessor, EqualizerReductionData
from Radio.util.dataTransmitter import Publisher
from Radio.dataProcessing.radioFrequency import RadioFrequency


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
        publisher = Publisher()
        player = AudioPlayer(publisher)

        p_send = Process(target=player.run)
        p_send.start()
        p_send.join()

        publisher.publish("https://stream.radiojar.com/whwyhz188a0uv")
        # CONFIRM MUSIC IS PLAYING
        time.sleep(10)

    def test_change_bass(self):
        publisher = Publisher()
        player = AudioPlayer(publisher)
        bass = 15

        # Could be that radio link is broken
        player.play("https://live.hunter.fm/80s_high")
        time.sleep(3)
        print(f"bass to: {bass}")
        player.set_equalizer(bass,
                             EqualizerReductionData(1, 2, 3, 4, -1, -1, -1))
        time.sleep(3)
        self.assertEqual(player.equalizer.get_amp_at_index(0), bass)