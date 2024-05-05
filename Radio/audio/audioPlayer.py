import time
import vlc

from Radio.dataProcessing.dataProcessor import EqualizerReductionData
from Radio.dataProcessing.radioFrequency import RadioFrequency
from Radio.util.util import Subscriber
from Radio.db.db import Database


class AudioPlayer(Subscriber):
    def __init__(self, publisher):
        self.noise_player = None  # Not implemented yet
        # TODO: extra publisher class and subscriber and use it as object
        self.publisher = publisher
        self.publisher.attach(self)
        self.noise = 30
        self.volume = 50

        self.equalizer: vlc.AudioEqualizer = vlc.AudioEqualizer()
        self.instance: vlc.Instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
        self.player: vlc.MediaPlayer = self.instance.media_player_new()

        self.database: Database = Database()
        self.stream: RadioFrequency = None
        self.stream_re: RadioFrequency = None
        self.re_active: bool = False

        self.set_equalizer([0,0,0,0,0,0,0,0])

    def update(self):
        content = self.publisher.get_content()
        if isinstance(content, RadioFrequency):
            # TODO: database always returns default values
            # self.stream = self.database.get_stream()
            # self.stream_re = self.database.get_stream_re()
            # self.re_active = self.database.get_re_active()
            print(f"STREAM: {self.stream}, {self.stream_re}")
            self.play(content)
        elif content == "stop":
            self.stop()
        elif isinstance(content, str):
            if "volume" in content:
                self.set_volume(int(content.strip("volume:")))
            elif "equalizer" in content:
                data = eval(content.strip("equalizer:"))
                self.set_equalizer(data)
        else:
            print("ERROR")

    def play(self, stream: RadioFrequency):
        if stream.re_active:
            radio_url = stream.radio_url_re
        else:
            radio_url = stream.radio_url
        if radio_url == "":
            return
        self.player.stop()
        # print(f"stream url: {radio_url}")
        media = self.instance.media_new(radio_url)
        media.get_mrl()
        self.player.audio_set_volume(self.volume)
        self.player.set_media(media)
        self.player.play()

    def stop(self):
        self.player.stop()

    def run(self):
        # TODO: add noise with encoder value
        self.player.play()

    def set_volume(self, volume):
        if self.player:
            self.player.audio_set_volume(volume)
        self.volume = volume

    def set_equalizer(self, equalizer_data: list):
        for index, value in enumerate(equalizer_data):
            self.equalizer.set_amp_at_index(value, index)
        self.player.set_equalizer(self.equalizer)

    def add_static_noise(self, level):
        self.noise_player.audio_set_volume(level)

    def play_radio_anouncement(self):
        pass


if __name__ == "__main__":
    audio_player = AudioPlayer(None)
    audio_player.play(RadioFrequency("München", 0, 100, "Energy München",
                                     "http://eu4.fastcast4u.com/proxy/carolanr2?mp=/1"))
    time.sleep(10)
