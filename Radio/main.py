from threading import Thread

from Radio.radio import Radio
from Radio.audioPlayer import AudioPlayer
from Radio.app import app
from Radio.db.db import Database
from Radio.collector import Collector
from Radio.led.ledStrip import LedStrip
import RPi.GPIO as GPIO
# from checkShutdown import ShutdownGpio

if __name__ == "__main__":
    GPIO.cleanup()
    db = Database()
    db.create()
    db.init()
    collector = Collector()

    # shutdownPin = ShutdownGpio()

    radio = Radio(mqtt=False, play_central=True, play_radio_speaker=True)
    audioPlayer = AudioPlayer(radio)
    ledStrip = LedStrip()

    radioThread = Thread(target=radio.run)
    collectorThread = Thread(target=collector.run)
    # shutdownThread = Thread(target=shutdownPin.run)
    ledThread = Thread(target=ledStrip.run)

    # shutdownThread.start()
    radioThread.start()
    collectorThread.start()
    ledThread.start()

    app.run(port=5555, host='0.0.0.0')
