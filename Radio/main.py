from threading import Thread
from radio import Radio
from audioPlayer import AudioPlayer
from app import app
from db.db import Database
from collector import Collector
#from web.dataWeb import DataGetter

if __name__ == "__main__":
    db = Database()
    db.create()
    db.init()
    collector = Collector()

    # usb_reader = USBReader()
    # dataGetter = DataGetter(radio)
    radio = Radio(mqtt=False, play_central=True, play_radio_speaker=True)
    audioPlayer = AudioPlayer(radio)

    radioThread = Thread(target=radio.run)
    collectorThread = Thread(target=collector.run)
    # readerThread = Thread(target=usb_reader.read_usb)

    radioThread.start()
    # readerThread.start()

    app.run(port=5555, host='0.0.0.0')