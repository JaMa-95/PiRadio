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
from Radio.util.util import is_raspberry, get_project_root
from Radio.util.daemon import Daemon

if is_raspberry():
    IS_RASPBERRY_PI = True
    mock = False


class RadioDaemon(Daemon):
    def __init__(self, pidfile, mock, collector_on, sole_web_control, debug, app) -> None:
        super().__init__(pidfile)
        self.stop_event = Event()
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

    def shutdown_server(self):
        if not self.app_process:
            return
        return
        pid = self.app_process.pid
        parent = psutil.Process(pid)
        for child in parent.children(recursive=True):
            child.kill()
        print("KILLED APP")
        
    def _start(self):
        print("STARTING THREADS")
        # INSTANCES
        publisher: Publisher = Publisher()
        self.collector = Collector(stop_event=self.stop_event, mock=mock, debug=self.debug)
        self.data_processor = DataProcessor(publisher, stop_event=self.stop_event)
        self.audioPlayer = AudioPlayer(publisher, stop_event=self.stop_event)
        self.on_off_button: OnOffButton = OnOffButton(stop_event=self.stop_event)
        self.fm_module: FmModule = FmModule(publisher, stop_event=self.stop_event)
         # THREADS
        self.on_off_thread = Thread(target=self.on_off_button.run)
        self.processor_thread = Thread(target=self.data_processor.run)
        self.collector_thread = Thread(target=self.collector.run)
        self.audio_thread = Thread(target=self.audioPlayer.run)
        #self.app_process = Process(target=app_run)
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
           pass
           # self.app_process.start()

        # JOIN
        self.processor_thread.join()
        self.audio_thread.join()
        self.on_off_thread.join()
        self.fm_module_thread.join()
        if self.collector_on:
            self.collector_thread.join()
        #if app:
        #    app_process.join()

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
