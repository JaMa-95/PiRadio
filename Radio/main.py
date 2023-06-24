from threading import Thread

from radio import Radio
from audioPlayer import AudioPlayer
from app import app
from db.db import Database
from collector import Collector
from led.ledStrip import LedStrip
from checkShutdown import ShutdownGpio

if __name__ == "__main__":
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
