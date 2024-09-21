import time
import psutil
from threading import Thread, Event
from multiprocessing import Process

import requests

from Radio.dataProcessing.dataProcessor import DataProcessor
from Radio.startup_button.onOffButton import OnOffButton
from Radio.util.dataTransmitter import Publisher
from Radio.audio.audioPlayer import AudioPlayer
from Radio.audio.tea5767 import FmModule
from Radio.app import run as app_run

from Radio.collector.collector import Collector
from Radio.util.util import is_raspberry, get_project_root, ThreadSafeInt, ThreadSafeList
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
        self.thread_stopped_counter: ThreadSafeInt = ThreadSafeInt()
        self.amount_threads: int = 0
        self.amount_stop_threads_names: ThreadSafeList = ThreadSafeList()
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
        while self.thread_stopped_counter.get() < self.amount_threads:
            print(f"STOPPING THREADS: {self.thread_stopped_counter.get()}")
            print(f"REMAINIGN: {self.amount_stop_threads_names.get()}")
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
        self.collector = Collector(stop_event=self.stop_event, mock=mock, debug=self.debug, 
                                   thread_stopped_counter=self.thread_stopped_counter, amount_stop_threads_names=self.amount_stop_threads_names)
        self.data_processor = DataProcessor(publisher, stop_event=self.stop_event, thread_stopped_counter=self.thread_stopped_counter,
                                            amount_stop_threads_names=self.amount_stop_threads_names)
        self.audio_player = AudioPlayer(publisher, stop_event=self.stop_event, thread_stopped_counter=self.thread_stopped_counter,
                                        amount_stop_threads_names=self.amount_stop_threads_names)
        self.on_off_button: OnOffButton = OnOffButton(stop_event=self.stop_event, thread_stopped_counter=self.thread_stopped_counter,
                                                      amount_stop_threads_names=self.amount_stop_threads_names)
        self.fm_module: FmModule = FmModule(publisher, stop_event=self.stop_event, mock=mock, 
                                            thread_stopped_counter=self.thread_stopped_counter,
                                            amount_stop_threads_names=self.amount_stop_threads_names)

         # THREADS
        self.on_off_thread = Thread(target=self.on_off_button.run)
        self.processor_thread = Thread(target=self.data_processor.run)
        self.collector_thread = Thread(target=self.collector.run)
        self.audio_thread = Thread(target=self.audio_player.run)
        self.app_process = Thread(target=app_run, args=(self.thread_stopped_counter, self.amount_stop_threads_names, ))
        self.fm_module_thread = Thread(target=self.fm_module.run)
        self.stop_thread = Thread(target=self.check_stop)
        print("STARTING THREADS")
        # START
        self.amount_stop_threads_names.append(self.data_processor.__class__.__name__)
        self.processor_thread.start()
        self.amount_threads += 1

        self.amount_stop_threads_names.append(self.audio_player.__class__.__name__)
        self.audio_thread.start()
        self.amount_threads += 1

        self.amount_stop_threads_names.append(self.on_off_button.__class__.__name__)
        self.on_off_thread.start()
        self.amount_threads += 1

        self.amount_stop_threads_names.append(self.fm_module.__class__.__name__)
        self.fm_module_thread.start()
        self.amount_threads += 1

        self.amount_stop_threads_names.append(self.check_stop.__name__)
        self.stop_thread.start()
        self.amount_threads += 1
        
        if self.collector_on:
            self.amount_stop_threads_names.append(self.collector.__class__.__name__)
            self.collector_thread.start()
            self.amount_threads += 1
        if self.app:
            self.amount_stop_threads_names.append(app_run.__name__)
            self.app_process.start()
            self.amount_threads += 1

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
        import psutil
        import time
        start_ = time.time()
        start = time.time()
        process = psutil.Process()
        while True:
            if True:
                if time.time() - start > 2:
                    # Get the current process
                    start = time.time()
                    # CPU usage of the current process
                    cpu_percent = process.cpu_percent(interval=1)
                    # Memory usage of the current process
                    memory_info = process.memory_info()
                    
                    print(f"CPU Usage of the script: {cpu_percent}%")
                    print("Memory Info of the script:")
                    print(f"Memory Usage: {memory_info.rss / (1024 * 1024):.2f} MB")
                    print("---------------------------")
                    # Calculate the average CPU usage over the last 10 seconds
                    if not hasattr(self, 'cpu_usage_list'):
                        self.cpu_usage_list = []
                    self.cpu_usage_list.append(cpu_percent)
                    elapsed_time = time.time() - start_
                    average_cpu_usage = sum(self.cpu_usage_list) / len(self.cpu_usage_list)
                    print(f"Average CPU Usage over the last {elapsed_time:.2f} seconds: {average_cpu_usage:.2f}%")
            if self.stop_event.is_set():
                self.thread_stopped_counter.increment()
                self.amount_stop_threads_names.delete(self.check_stop.__name__)
                break
            with open(self.path_stop_file, "r") as file:
                content = file.read()
                if content != "":
                    self.stop()
                    self.thread_stopped_counter.increment()
                    self.amount_stop_threads_names.delete(self.stop_thread.__class__.__name__)
                    break
            time.sleep(0.3)



if __name__ == "__main__":
    daemon = RadioDaemon("/tmp/PiRadio.pid", mock=False, collector_on=True, sole_web_control=False, debug=False, app=True)
    daemon.start()
