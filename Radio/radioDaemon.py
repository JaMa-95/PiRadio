import time
import psutil
from threading import Thread, Event
from multiprocessing import Process

from Radio.dataProcessing.dataProcessor import DataProcessor
from Radio.startup_button.on_off_button import OnOffButton
from Radio.util.dataTransmitter import Publisher
from Radio.audio.audioPlayer import AudioPlayer
from Radio.audio.tea5767 import FmModule
from Radio.app import run as app_run

from Radio.collector.collector import Collector
from Radio.util.util import is_raspberry
from Radio.util.daemon import Daemon

if is_raspberry():
    IS_RASPBERRY_PI = True
    mock = False


class RadioDaemon(Daemon):
    def __init__(self, mock, collector_on, sole_web_control, debug, app) -> None:
        self.stop_event = Event()
        self.mock = mock
        self.collector_on = collector_on
        self.sole_web_control = sole_web_control
        self.debug = debug
        self.app = app

        self._reset_stop_file()

        publisher: Publisher = Publisher()
        self.collector = Collector(stop_event=self.stop_event, mock=mock, debug=debug)
        self.data_processor = DataProcessor(publisher, stop_event=self.stop_event)
        self.audioPlayer = AudioPlayer(publisher, stop_event=self.stop_event)
        self.on_off_button: OnOffButton = OnOffButton(stop_event=self.stop_event)
        self.fm_module: FmModule = FmModule(publisher, stop_event=self.stop_event)

        # THREADS
        self.on_off_thread = Thread(target=self.on_off_button.run)
        self.processor_thread = Thread(target=self.data_processor.run)
        self.collector_thread = Thread(target=self.collector.run)
        self.audio_thread = Thread(target=self.audioPlayer.run)
        self.app_process = Process(target=app_run)
        self.fm_module_thread = Thread(target=self.fm_module.run)
        # self.stop_thread = Thread(target=self.check_stop, args=(self.app_process,))

    def _reset_stop_file(self):
        with open("stop.txt", "w") as file:
            file.write("")

    def _stop(self):
        print("ASDDDDDDDDDDDDDDDDDDDDd")
        self.shutdown_server(self.app_process)
        self.stop_event.set()

    def shutdown_server(self, process: Process):

        pid = process.pid
        parent = psutil.Process(pid)
        for child in parent.children(recursive=True):
            child.kill()
        print("KILLED APP")
        
    def _start(self):
        # START
        self.processor_thread.start()
        self.audio_thread.start()
        self.on_off_thread.start()
        self.fm_module_thread.start()
        # self.stop_thread.start()
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
        #if app:
        #    app_process.join()

        # self.stop_thread.join()
        print("EEEEEEEEEEEEEEEEEEEEEEEEND")

    def run(self):
        print("Starting threads")
        self._start()
        self.check_stop()
        
    def check_stop(self):
        while True:
            with open("stop.txt", "r") as file:
                content = file.read()
                if content != "":
                    print("STOPPING")
                    self.stop()
                    print("STOPPED")
                    break
            time.sleep(1)
