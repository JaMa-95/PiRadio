from db.db import Database
from flask_cors import CORS

from flask import Flask, render_template, request, jsonify
from turbo_flask import Turbo

app = Flask(__name__)
turbo = Turbo(app)
CORS(app)

db = Database()


@app.route("/")
def home():
    db.create()
    db.insert_volume(10)
    db.insert_stream("abc")
    db.insert_pos_lang_mittel_kurz(21)
    db.insert_pos_ukw(55)
    db.insert_button_ukw(22)
    db.insert_button_lang(100)
    db.insert_button_mittel(99)
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


@app.route('/data')
def get_data():
    return {
        "volume": db.get_volume(),
        "stream": db.get_stream(),
        "button_on_off": db.get_button_on_off_web(),
        "button_lang": db.get_button_lang_web(),
        "button_mittel": db.get_button_mittel_web(),
        "button_kurz": db.get_button_kurz_web(),
        "button_ukw": db.get_button_ukw_web(),
        "button_spr": db.get_button_spr_mus_web(),
        "pos_lang_mittel_kurz": db.get_pos_lang_mittel_kurz(),
        "pos_ukw_spr": db.get_pos_ukw(),
        "radio_name": db.get_radio_name()
    }


@app.route('/web_control', methods=['GET', 'POST'])
def switch_web_control():
    state = request.form["state"]
    db.replace_web_control_value(state)
    return jsonify({'result': 'OK'})


@app.route('/button_clicked/<name>/<state>', methods=['GET', 'POST'])
def button_clicked(name, state):
    # state = request.form["state"]
    if "on" in name:
        db.replace_button_on_off(state)
    elif "lang" in name:
        db.replace_button_lang(state)
    elif "mittel" in name:
        db.replace_button_mittel(state)
    elif "kurz" in name:
        db.replace_button_kurz(state)
    elif "ukw" in name:
        db.replace_button_ukw(state)
    elif "spr" in name:
        db.replace_button_spr_mus(state)
    else:
        return f"Button name invalid: {name}", 400
    return jsonify({'result': 'OK'})


@app.route('/pos_lang_kurz_mittel/<value>', methods=['GET', 'POST'])
def pos_changed(value):
    db.replace_pos_lang_mittel_kurz(value)
    return jsonify({'result': 'OK'})


@app.route('/volume/<value>', methods=['GET', 'POST'])
def volume_changed(value):
    db.replace_volume(value)
    return jsonify({'result': 'OK'})


if __name__ == "__main__":
    app.run(port=5000, host='0.0.0.0')
