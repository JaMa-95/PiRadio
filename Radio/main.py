import sys
import os
import time
import psutil
from threading import Thread, Event
from multiprocessing import Process

from Radio.dataProcessing.dataProcessor import DataProcessor
from Radio.startup_button.on_off_button import OnOffButton
from Radio.util.dataTransmitter import Publisher

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from Radio.audio.audioPlayer import AudioPlayer
from Radio.audio.tea5767 import FmModule
from Radio.app import run as app_run

from Radio.collector.collector import Collector
from Radio.util.util import is_raspberry, get_args
from Radio.radioDaemon import RadioDaemon

if is_raspberry():
    IS_RASPBERRY_PI = True
    mock = False
    import RPi.GPIO as GPIO


if __name__ == "__main__":
    try:
        daemon = RadioDaemon(*get_args())
        daemon.start()
        sys.exit(0)
    except KeyboardInterrupt:
        daemon.stop()
        sys.exit(0)
