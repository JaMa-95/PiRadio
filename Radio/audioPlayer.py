import time
import vlc

from Radio.radioFrequency import RadioFrequency
from Radio.util.util import Subscriber


class AudioPlayer(Subscriber):
    def __init__(self, publisher):
        self.noise_player = None  # Not implemented yet
        self.publisher = publisher
        self.publisher.attach(self)
        self.noise = 30
        self.volume = 50

        self.equalizer = vlc.AudioEqualizer()
        self.instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
        self.player = self.instance.media_player_new()

        self.set_treble(0)
        self.set_bass(0)

    def update(self):
        content = self.publisher.get_content()
        if type(content) == RadioFrequency:
            self.play(content)
        elif content == "stop":
            self.stop()
        elif isinstance(content, str):
            if "volume" in content:
                self.set_volume(int(content.strip("volume:")))
            elif "bass" in content:
                self.set_bass(int(content.strip("bass:")))
            elif "treble" in content:
                self.set_treble(int(content.strip("treble:")))
        else:
            print("ERROR")

    def play(self, stream: RadioFrequency):
        self.player.stop()
        print(f"stream url: {stream.radio_url}")
        media = self.instance.media_new(stream.radio_url)
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

    def set_bass(self, bass):
        print(f"bass: {bass}")
        self.equalizer.set_amp_at_index(bass, 0)  # 60 Hz
        self.equalizer.set_amp_at_index(bass / 2, 1)  # 170 Hz
        self.equalizer.set_amp_at_index(bass / 3, 2)  # 310 Hz
        self.equalizer.set_amp_at_index(bass / 4, 3)  # 600 Hz
        self.player.set_equalizer(self.equalizer)

    def set_treble(self, treble):
        print(f"treble: {treble}")
        treble = 0
        self.equalizer.set_amp_at_index(treble / 4, 4)  # 1 kHz
        self.equalizer.set_amp_at_index(treble / 3, 5)  # 3 kHz
        self.equalizer.set_amp_at_index(treble / 2, 6)  # 6 kHz
        self.equalizer.set_amp_at_index(treble, 7)  # 12 kHz
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
