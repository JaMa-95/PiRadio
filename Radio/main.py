import sys
import os
from multiprocessing import Process
from threading import Thread

from Radio.dataProcessing.dataProcessor import DataProcessor
from Radio.util.dataTransmitter import Publisher

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from Radio.audio.audioPlayer import AudioPlayer
from Radio.app import run as app_run

from Radio.collector.collector import Collector
from Radio.util.util import is_raspberry

mock = True
IS_RASPBERRY_PI = False
if is_raspberry():
    IS_RASPBERRY_PI = True
    import RPi.GPIO as GPIO

def start_app() -> bool:
    if len(sys.argv) > 1:
        if sys.argv[1] == "--app=1":
            return True
    return False

if __name__ == "__main__":
    if IS_RASPBERRY_PI:
        mock = False
    
    start_app = start_app()
       
    publisher: Publisher = Publisher()
    collector = Collector(mock=mock)
    data_processor = DataProcessor(publisher)
    audioPlayer = AudioPlayer(publisher)

    processor_thread = Thread(target=data_processor.run)
    collector_thread = Thread(target=collector.run)
    audio_thread = Thread(target=audioPlayer.run)
    app_thread = Thread(target=app_run)

    SOLE_WEB_CONTROL = True
    try:
        if not SOLE_WEB_CONTROL:
            collector_thread.start()
        processor_thread.start()
        audio_thread.start()

        if start_app:
            app_thread.start()
        if not SOLE_WEB_CONTROL:
            collector_thread.join()
        processor_thread.join()
        audio_thread.join()
        if start_app:
            app_thread.join()
    finally:
        # TODO: stop all threads
        pass
