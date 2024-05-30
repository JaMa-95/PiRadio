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
        publisher = Publisher()
        processor = DataProcessor(publisher)
        player = AudioPlayer(publisher)

        # Could be that radio link is broken
        player.play("https://relax.stream.publicradio.org/relax.mp3?srcid")
        time.sleep(7)
        self.assertTrue(player.player.is_playing())

    def test_play_music_pub_sub(self):
        publisher = Publisher()
        player = AudioPlayer(publisher)

        processor = DataProcessor(publisher)
        b_process = Process(target=processor.run)
        p_send = Process(target=player.run)
        p_send.start()
        b_process.start()
        p_send.join()
        b_process.join()
        publisher.publish("volume:50")
        publisher.publish("stream:https://relax.stream.publicradio.org/relax.mp3?srcid")
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


if __name__ == '__main__':
    player = TestAudioPlayer()
    player.test_play_music_pub_sub()