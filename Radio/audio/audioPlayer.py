import time

from mpd import MPDClient, ProtocolError, ConnectionError
from threading import Event

from Radio.dataProcessing.radioFrequency import RadioFrequency
from Radio.db.db import Database
from Radio.util.dataTransmitter import Subscriber
from Radio.util.util import ThreadSafeInt, ThreadSafeList


class AudioPlayer(Subscriber):
    def __init__(self, publisher, stop_event: Event = None, thread_stopped_counter: ThreadSafeInt = None, 
                 amount_stop_threads_names: ThreadSafeList=None):
        self._stop_event = stop_event
        self.noise_player = None
        self.thread_stopped_counter: ThreadSafeInt = thread_stopped_counter
        self.amount_stop_threads_names: ThreadSafeList = amount_stop_threads_names
        self.publisher = publisher
        self.publisher.attach(self)
        self.database: Database = Database()
        self.noise = 30
        self.volume = self.database.get_volume()

        self.client = MPDClient()                   # create client object
        self.client.timeout = None                  # network timeout in seconds (floats allowed), default: None
        self.client.idletimeout = None              # timeout for fetching the result of the idle command is handled seperately, default: None
        self.connect()
        self.set_volume(self.volume)

        print("Audio Player started")
        # self.set_equalizer([0, 0, 0, 0, 0, 0, 0, 0])

    def connect(self):
        self.client.connect("localhost", 6600)
    
    def stop(self):
        self.publisher.detach()
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
        try:
            self.client.clear()
            self.client.add(url)  # add the URL stream to the playlist
            self.client.play()                               # start playing the stream
        except ProtocolError:
            print("Error: Protocoll error with url: ", url)
            return

    def run(self):
        while True:
            try:
                status = self.client.status()
            except ConnectionError:
                self.client.connect("localhost", 6600)  # connect to localhost:6600
                print("MPD connection error")
                time.sleep(1)
                continue
            try:
                if status['state'] == 'play':
                    current_song = self.client.currentsong()
                    self.database.replace_song_name(self.get_song_title(current_song))
                    self.database.replace_song_station(self.get_station_name(current_song))
            except KeyError:
                pass
                    
            if self._stop_event.is_set():
                print("STOP EVENT AUDIO PLAYER")
                self.stop()
                self.thread_stopped_counter.increment()
                self.amount_stop_threads_names.delete(self.__class__.__name__)
                break
            time.sleep(1)

    def get_song_title(self, current_song):
        try:
            return current_song["title"]
        except KeyError as e:
            return "Unknown"
    
    def get_station_name(self, current_song):
        try:
            return current_song["name"]
        except KeyError as e:
            return "Unknown"
        

    def set_volume(self, volume):
        try:
            self.client.setvol(volume)
        except ConnectionError:
            print("MPD connection error")
            return

    def set_equalizer(self, equalizer_data: list):
        print(f"SET EQ: {equalizer_data}")
        return None
        for index, value in enumerate(equalizer_data):
            if value != -1:
                self.equalizer.set_amp_at_index(value, index)
        self.player.set_equalizer(self.equalizer)

    def add_static_noise(self, level):
        self.noise_player.audio_set_volume(level)

    def play_radio_anouncement(self):
        pass

    def is_valid(self, url: str) -> bool:
        self.client.clear()
        self.client.add(url)
        self.client.play()
        time.sleep(0.2)
        self.client.status()
        self.client.stop()
        if "error" in self.client.status():
            return False
        return True


if __name__ == "__main__":
    audio_player = AudioPlayer(None)
    audio_player.play(RadioFrequency("München", 0, 100, "Energy München",
                                     "http://eu4.fastcast4u.com/proxy/carolanr2?mp=/1"))
    time.sleep(10)
