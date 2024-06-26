import sys
import os
import time
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

IS_RASPBERRY_PI = False
if is_raspberry():
    IS_RASPBERRY_PI = True
    import RPi.GPIO as GPIO

if __name__ == "__main__":
    if IS_RASPBERRY_PI:
        GPIO.cleanup()
        GPIO.setup(6, GPIO.OUT)
        GPIO.output(6, True)
        GPIO.setup(5, GPIO.OUT)
        GPIO.output(5, True)

    publisher: Publisher = Publisher()
    # shutdownPin = ShutdownGpio()
    collector = Collector(mock=True)
    data_processor = DataProcessor(publisher)
    audioPlayer = AudioPlayer(publisher)

    processor_thread = Thread(target=data_processor.run)
    collector_thread = Process(target=collector.run)
    audio_thread = Process(target=audioPlayer.run)
    app_thread = Process(target=app_run)

    SOLE_WEB_CONTROL = True
    try:
        if not SOLE_WEB_CONTROL:
            collector_thread.start()
        processor_thread.start()
        audio_thread.start()
        app_thread.start()
        print("All threads are started")
        if not SOLE_WEB_CONTROL:
            collector_thread.join()
        processor_thread.join()
        audio_thread.join()
        app_thread.join()
        print("All threads are done")
    finally:
        collector_thread.terminate()
        processor_thread.terminate()
        app_thread.terminate()
        app_thread.terminate()
