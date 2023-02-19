from threading import Thread
from radio import Radio, USBReader
from audioPlayer import AudioPlayer
from app import app
from db.db import Database
#from web.dataWeb import DataGetter

if __name__ == "__main__":
    db = Database()
    db.create()
    db.init()

    usb_reader = USBReader()
    #dataGetter = DataGetter(radio)
    radio = Radio(mqtt=False, play_central=True, play_radio_speaker=True)
    audioPlayer = AudioPlayer(radio)

    radioThread = Thread(target=radio.check_commands)
    readerThread = Thread(target=usb_reader.read_usb)

    radioThread.start()
    readerThread.start()

    app.run(port=5555, host='0.0.0.0')