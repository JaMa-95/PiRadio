import time

import vlc

from Radio.dataProcessing.radioFrequency import RadioFrequency
from Radio.db.db import Database
from Radio.util.dataTransmitter import Subscriber


class AudioPlayer(Subscriber):
    def __init__(self, publisher):
        self.noise_player = None
        self.publisher = publisher
        self.publisher.attach(self)
        self.noise = 30
        self.volume = 50

        self.equalizer: vlc.AudioEqualizer = vlc.AudioEqualizer()
        self.instance: vlc.Instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
        self.player: vlc.MediaPlayer = self.instance.media_player_new()
        self.player.set_equalizer(self.equalizer)

        self.database: Database = Database()
        print("Audio Player started")
        # self.set_equalizer([0, 0, 0, 0, 0, 0, 0, 0])

    def update(self):
        content = self.publisher.get_content()
        if "stream:" in content:
            url = content.strip("stream:")
            self.play(url)
        elif content == "stop":
            self.stop()
        elif "volume" in content:
            self.set_volume(int(content.strip("volume:")))
        elif "equalizer" in content:
            data = eval(content.strip("equalizer:"))
            self.set_equalizer(data)
        else:
            pass
            # print(f"unknown content at audio player: {content}")

    def play(self, url: str):
        self.player.stop()
        media = self.instance.media_new(url)
        media.get_mrl()
        self.player.audio_set_volume(self.volume)
        self.player.set_media(media)
        self.player.play()

    def stop(self):
        self.player.stop()

    def run(self):
        # TODO: add noise with encoder value
        # self.player.play()
        # check playing if yes play
        pass

    def set_volume(self, volume):
        if self.player:
            self.player.audio_set_volume(volume)
        self.volume = volume

    def set_equalizer(self, equalizer_data: list):
        for index, value in enumerate(equalizer_data):
            self.equalizer.set_amp_at_index(value, index)
        self.player.set_equalizer(self.equalizer)
        for index, a in enumerate(equalizer_data):
            amp = self.equalizer.get_amp_at_index(index)
            print(amp)

    def add_static_noise(self, level):
        self.noise_player.audio_set_volume(level)

    def play_radio_anouncement(self):
        pass


if __name__ == "__main__":
    audio_player = AudioPlayer(None)
    audio_player.play(RadioFrequency("München", 0, 100, "Energy München",
                                     "http://eu4.fastcast4u.com/proxy/carolanr2?mp=/1"))
    time.sleep(10)
