import time
import vlc
from radioFrequency import RadioFrequency
from util import Subscriber


class AudioPlayer(Subscriber):

    def __init__(self, publisher):
        self.publisher = publisher
        self.publisher.attach(self)
        self.noise = 30
        self.volume = 50

        self.instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
        self.player = self.instance.media_player_new()

    def update(self):
        content = self.publisher.get_content()
        print(f"CONTENT: {content}")
        print(f"TYPE: {type(content)}")
        if type(content) == RadioFrequency:
            self.play(content)
        elif type(content) == str:
            self.stop()
        elif type(content) == int:
            self.set_volume(content)
        else:
            print("ERROR")

    def play(self, stream: RadioFrequency):
        self.player.stop()
        media = self.instance.media_new(stream.radio_url)
        media.get_mrl()
        self.player.audio_set_volume(self.volume)
        self.player.set_media(media)
        self.player.play()

    def stop(self):
        print("STOPPING")
        self.player.stop()

    def run(self):
        # TODO: add noise with encoder value
        self.player.play()

    def set_volume(self, volume):
        if self.player:
            self.player.audio_set_volume(volume)
        self.volume = volume

    def add_static_noise(self, level):
        self.noise_player.audio_set_volume(level)

    def play_radio_anouncement(self):
        pass


if __name__ == "__main__":
    audio_player = AudioPlayer(
        RadioFrequency("München", 0, 100, "Energy München", "http://eu4.fastcast4u.com/proxy/carolanr2?mp=/1"), 1)
    # audio_player.play()
    audio_player.start()
    # audio_player_thread.start()
    time.sleep(10)
