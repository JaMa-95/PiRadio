from threading import Thread
from radio import Radio, USBReader
from audioPlayer import AudioPlayer
from app import app
from db.db import Database
#from web.dataWeb import DataGetter

if __name__ == "__main__":
    db = Database()
    db.create()
    db.test_data()

    app.run()

    usb_reader = USBReader()
    #dataGetter = DataGetter(radio)
    radio = Radio(mqtt=True, play_central=True, play_speaker=True)
    audioPlayer = AudioPlayer(radio)

    radioThread = Thread(target=radio.check_commands)
    readerThread = Thread(target=usb_reader.read_usb)

    radioThread.start()
    readerThread.start()