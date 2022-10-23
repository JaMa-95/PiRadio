from flask import Flask, redirect, url_for, render_template

from threading import Thread
from radio import Radio, USBReader
from audioPlayer import AudioPlayer
from web.dataWeb import DataGetter


app = Flask(__name__)


def init():
    usb_reader = USBReader()
    radio = Radio()
    audioPlayer = AudioPlayer(radio)
    dataGetter = DataGetter(radio)

    radioThread = Thread(target=radio.check_commands)
    readerThread = Thread(target=usb_reader.read_usb)

    radioThread.start()
    readerThread.start()

@app.route("/")
def home():
    data_getter = DataGetter()
    data_getter.update()
    return render_template("index.html", volume=data_getter.volume, stream=data_getter.stream,
                           button_on_off=data_getter.button_on_off,
                           button_lang=data_getter.button_lang, button_mittel=data_getter.button_mittel,
                           button_kurz=data_getter.button_kurz,
                           button_ukw=data_getter.button_ukw, button_spr=data_getter.button_spr,
                           pos_lang_mittel_kurz=data_getter.pos_lang_mittel_kurz, pos_ukw_spr=data_getter.pos_ukw_spr)


@app.route("/<name>")
def user(name):
    return f"Hello {name}!"


@app.route("/admin")
def admin():
    return redirect(url_for("user", name="Admin!"))  # Now we when we go to /admin we will redirect to user with the argument "Admin!"


if __name__ == "__main__":

    app.run()
