from flask import Flask, redirect, url_for, render_template
from turbo_flask import Turbo
import random
import threading
import time
from Radio.db.db import Database

app = Flask(__name__)
turbo = Turbo(app)


@app.route("/")
def home():
    db = Database()
    db.create()
    db.insert_volume(10)
    db.insert_stream("abc")
    db.insert_pos_lang_mittel_kurz(21)
    db.insert_pos_ukw(55)
    db.insert_button_ukw(22)
    db.insert_button_lang(100)
    db.insert_butto_mittel(99)
    db.insert_button_kurz(98)
    db.insert_button_on_off(97)
    db.insert_button_spr_mus(96)
    return render_template("index.html",
                           volume=db.get_volume(),
                           stream=db.get_stream(),
                           button_on_off=db.get_button_on_off_web(),
                           button_lang=db.get_button_lang_web(),
                           button_mittel=db.get_button_mittel_web(),
                           button_kurz=db.get_button_kurz_web(),
                           button_ukw=db.get_button_ukw_web(),
                           button_spr=db.get_button_spr_mus_web(),
                           pos_lang_mittel_kurz=db.get_pos_lang_mittel_kurz(),
                           pos_ukw_spr=db.get_pos_ukw())


@app.route("/<name>")
def user(name):
    return f"Hello {name}!"


@app.context_processor
def inject_load():
    return {
        "volume": random.random(),
        "stream": random.random(),
        "button_on_off": random.random(),
        "button_lang": random.random(),
        "button_mittel": random.random(),
        "button_kurz": random.random(),
        "button_ukw": random.random(),
        "button_spr": random.random(),
        "pos_lang_mittel_kurz": random.random(),
        "pos_ukw_spr": random.random()
    }


@app.before_first_request
def before_first_request():
    threading.Thread(target=update_load).start()


def update_load():
    with app.app_context():
        while True:
            time.sleep(2)
            turbo.push(turbo.replace(render_template('loadavg.html'), 'load'))


@app.route("/admin")
def admin():
    return redirect(url_for("user",
                            name="Admin!"))  # Now we when we go to /admin we will redirect to user with the argument "Admin!"


if __name__ == "__main__":
    app.run()
