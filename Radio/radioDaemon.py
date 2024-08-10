import time
import psutil
from threading import Thread, Event
from multiprocessing import Process

import requests

from Radio.dataProcessing.dataProcessor import DataProcessor
from Radio.startup_button.on_off_button import OnOffButton
from Radio.util.dataTransmitter import Publisher
from Radio.audio.audioPlayer import AudioPlayer
from Radio.audio.tea5767 import FmModule
from Radio.app import run as app_run

from Radio.collector.collector import Collector
from Radio.util.util import is_raspberry, get_project_root, ThreadSafeInt
from Radio.util.daemon import Daemon

mock = True
IS_RASPBERRY_PI = False
if is_raspberry():
    IS_RASPBERRY_PI = True
    mock = False


class RadioDaemon(Daemon):
    def __init__(self, pidfile, mock, collector_on, sole_web_control, debug, app) -> None:
        super().__init__(pidfile)
        self.stop_event = Event()
        self.thread_stopped_counter = ThreadSafeInt()
        self.amount_stop_threads: int = 5
        self.mock = mock
        self.collector_on = collector_on
        self.sole_web_control = sole_web_control
        self.debug = debug
        self.app = app
        self.app_process = None
        self.path_stop_file = get_project_root() / "stop.txt"

        self._reset_stop_file()
        # self.stop_thread = Thread(target=self.check_stop, args=(self.app_process,))

    def _reset_stop_file(self):
        with open(self.path_stop_file, "w") as file:
            file.write("")

    def _stop(self):
        self.shutdown_server()
        self.stop_event.set()
        while self.thread_stopped_counter.get() < self.amount_stop_threads:
            print(f"STOPPING THREADS: {self.thread_stopped_counter.get()}")
            time.sleep(0.1)

    def shutdown_server(self):
        if not self.app_process:
            print("NO APP PROCESS")
            return
        response = requests.get('http://localhost:8000/shutdown').content
        print(f"Reponse server shutdown: {response}")
        
    def _start(self):
        print("STARTING THREADS")
        # INSTANCES
        publisher: Publisher = Publisher()
        self.collector = Collector(stop_event=self.stop_event, mock=mock, debug=self.debug, thread_stopped_counter=self.thread_stopped_counter)
        self.data_processor = DataProcessor(publisher, stop_event=self.stop_event, thread_stopped_counter=self.thread_stopped_counter)
        self.audio_player = AudioPlayer(publisher, stop_event=self.stop_event, thread_stopped_counter=self.thread_stopped_counter)
        self.on_off_button: OnOffButton = OnOffButton(stop_event=self.stop_event, thread_stopped_counter=self.thread_stopped_counter)
        self.fm_module: FmModule = FmModule(publisher, stop_event=self.stop_event, mock=mock, thread_stopped_counter=self.thread_stopped_counter)

         # THREADS
        self.on_off_thread = Thread(target=self.on_off_button.run)
        self.processor_thread = Thread(target=self.data_processor.run)
        self.collector_thread = Thread(target=self.collector.run)
        self.audio_thread = Thread(target=self.audio_player.run)
        self.app_process = Thread(target=app_run)
        self.fm_module_thread = Thread(target=self.fm_module.run)
        self.stop_thread = Thread(target=self.check_stop)
        print("STARTING THREADS")
        # START
        self.processor_thread.start()
        self.audio_thread.start()
        self.on_off_thread.start()
        self.fm_module_thread.start()
        self.stop_thread.start()
        if self.collector_on:
            self.collector_thread.start()
        if self.app:
           self.app_process.start()

        # JOIN
        self.processor_thread.join()
        self.audio_thread.join()
        self.on_off_thread.join()
        self.fm_module_thread.join()
        if self.collector_on:
            self.collector_thread.join()
        if self.app:
            self.app_process.join()

        self.stop_thread.join()
        print("ALL THREADS FINISHED")

    def run(self):
        import sys
        sys.stderr.write("Starting daemon\n")
        self._start()
        print("CLOSING")
        
    def check_stop(self):
        while True:
            with open(self.path_stop_file, "r") as file:
                content = file.read()
                if content != "":
                    self.stop()
                    break
            time.sleep(0.1)


if __name__ == "__main__":
    daemon = RadioDaemon("/tmp/PiRadio.pid", mock=False, collector_on=True, sole_web_control=False, debug=False, app=True)
    daemon.start()
