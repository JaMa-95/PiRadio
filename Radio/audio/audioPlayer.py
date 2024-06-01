import time

from mpd import MPDClient

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

        self.client = MPDClient()               # create client object
        self.client.timeout = 10                # network timeout in seconds (floats allowed), default: None
        self.client.idletimeout = None          # timeout for fetching the result of the idle command is handled seperately, default: None
        self.client.connect("localhost", 6600)  # connect to localhost:6600

        self.database: Database = Database()
        print("Audio Player started")
        # self.set_equalizer([0, 0, 0, 0, 0, 0, 0, 0])

    def __del__(self):
        self.client.stop()
        self.client.disconnect()
        print("Audio Player stopped")

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
        print("Playing: ", url)
        self.client.clear()
        self.client.add(url)  # add the URL stream to the playlist
        self.client.play()                               # start playing the stream

    def stop(self):
        self.client.stop()

    def run(self):
        while True:
            status = self.client.status()
            if status['state'] == 'play':
                current_song = self.client.currentsong()
                self.database.replace_song_name(current_song["name"])
                self.database.replace_song_station(current_song["file"])
            time.sleep(1)

    def set_volume(self, volume):
        self.client.setvol(volume)

    def set_equalizer(self, equalizer_data: list):
        return None
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
