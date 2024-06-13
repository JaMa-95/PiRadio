import sys
import os
from threading import Thread

from Radio.dataProcessing.dataProcessor import DataProcessor
from Radio.startup_button.on_off_button import OnOffButton
from Radio.util.dataTransmitter import Publisher

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from Radio.audio.audioPlayer import AudioPlayer
from Radio.app import run as app_run

from Radio.collector.collector import Collector
from Radio.util.util import is_raspberry
import datetime

if is_raspberry():
    IS_RASPBERRY_PI = True
    mock = False
    import RPi.GPIO as GPIO


def get_args(mock_=False, collector_on_=True, sole_web_control_=False, debug_=False, app_=True):
    if len(sys.argv) > 1:
        for arg in sys.argv:
            if arg == "--collector=0":
                collector_on_ = False
            if arg == "--sole_web=1":
                sole_web_control_ = True
            if arg == "--mock=1":
                mock_ = True
            if arg == "--debug=1":
                debug_ = True
            if arg == "--app=0":
                app_ = False
    return mock_, collector_on_, sole_web_control_, debug_, app_


def write():
    import time
    while True:
        with open("output.txt", "w") as file:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(current_time)
        time.sleep(1)


if __name__ == "__main__":
    mock, collector_on, sole_web_control, debug, app = get_args()
    # CLASSES
    publisher: Publisher = Publisher()
    collector = Collector(mock=mock, debug=debug)
    data_processor = DataProcessor(publisher)
    audioPlayer = AudioPlayer(publisher)
    on_off_button: OnOffButton = OnOffButton()

    # THREADS
    on_off_thread = Thread(target=on_off_button.run)
    processor_thread = Thread(target=data_processor.run)
    collector_thread = Thread(target=collector.run)
    audio_thread = Thread(target=audioPlayer.run)
    app_thread = Thread(target=app_run)
    write_thread = Thread(target=write)

    try:
        # START
        processor_thread.start()
        audio_thread.start()
        on_off_thread.start()
        if collector_on:
            collector_thread.start()
        if debug:
            write_thread.start()
        if app:
            app_thread.start()

        # JOIN
        processor_thread.join()
        audio_thread.join()
        on_off_thread.join()
        if collector_on:
            collector_thread.join()
        if debug:
            write_thread.join()
        if app:
            app_thread.join()
    finally:
        # TODO: stop all threads
        pass
