import datetime
import json
import time
from dataclasses import dataclass
import RPi.GPIO as GPIO

from radioFrequency import RadioFrequency, KurzFrequencies, LangFrequencies, MittelFrequencies, UKWFrequencies, \
    SprFrequencies, TaFrequencies
from button import RadioButtonsRaspi
from db.db import Database
from raspberry import Raspberry
from mqtt.mqttBroker import MqttBroker
from led.ledStrip import LedStrip, LedData


# TODO: Add web control
@dataclass
class Speakers:
    play_radio: bool = True
    play_central: bool = False

    _change_wait: bool = datetime.datetime.now()

    def change(self, play_central: bool, play_radio: bool):
        self.play_radio = play_radio
        self.play_central = play_central

    def change_once(self):
        now = datetime.datetime.now()
        change_delta = now - self._change_wait
        if change_delta.seconds > 2:
            self._change_wait = now
            if self.play_radio and self.play_central:
                print("CHANGE SPEAKER TO CENTRAL")
                self.play_radio = False
            elif self.play_radio:
                print("CHANGE SPEAKER TO CENTRAL/RADIO")
                self.play_central = True
            elif self.play_central:
                print("CHANGE SPEAKER TO RADIO")
                self.play_central = False
                self.play_radio = True


class Radio:
    def __init__(self, mqtt: bool, play_central: bool, play_radio_speaker: bool) -> None:
        # init pub
        self.__subscribers = []
        self.__content = None

        self.raspberry = Raspberry()
        self.playing = False
        self.on = False

        self.amplifier_switch_pin = 4
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.amplifier_switch_pin, GPIO.OUT)

        self.speakers = Speakers(play_radio=play_radio_speaker, play_central=play_central)

        self.radio_buttons = RadioButtonsRaspi()
        self.radio_lock: bool = False

        self.current_stream: RadioFrequency = RadioFrequency("", 0, 0, "", "")
        self.current_command = {"buttonOnOff": None, "buttonLang": None, "buttonMittel": None, "buttonKurz": None,
                                "buttonUKW": None, "buttonSprMus": None, "volume": None, "posLangKurzMittel": None,
                                "buttonTa": None,
                                "posUKW": None, "treble": None, "bass": None}
        self.old_command = {"buttonOnOff": None, "buttonLang": None, "buttonMittel": None, "buttonKurz": None,
                            "buttonUKW": None, "buttonSprMus": None, "volume": None, "posLangKurzMittel": None,
                            "buttonTa": None,
                            "posUKW": None, "treble": None, "bass": None}
        self.currentCommandString = None
        self.broker: MqttBroker = None
        self.mqtt = mqtt
        if mqtt:
            self.connect_mqtt()

        self.ledData = LedData.instance()
        self.ledStrip = LedStrip()
        self.db = Database()

        self.volume_old = 0
        self.volume_min = 0
        self.volume_max = 0
        self.volume_on = False
        self.bass_min = 0
        self.bass_max = 0
        self.bass_on = False
        self.treble_min = 0
        self.treble_max = 0
        self.treble_on = False

        self.pin_frequencies = None
        self.pin_volume = None
        self.pin_bass = None
        self.pin_treble = None

        self.settings: dict = None
        self.load_settings()

    def load_settings(self):
        with open('data/settings.json') as f:
            self.settings = json.load(f)
        self.volume_min = self.settings["volume"]["min"]
        self.volume_max = self.settings["volume"]["max"]
        self.volume_on = self.settings["volume"]["on"]
        self.pin_volume = self.settings["volume"]["pin"]
        self.bass_min = self.settings["bass"]["min"]
        self.bass_max = self.settings["bass"]["max"]
        self.bass_on = self.settings["bass"]["on"]
        self.pin_bass = self.settings["bass"]["pin"]
        self.treble_min = self.settings["treble"]["min"]
        self.treble_max = self.settings["treble"]["max"]
        self.treble_on = self.settings["treble"]["on"]
        self.pin_treble = self.settings["treble"]["pin"]
        self.pin_frequencies = self.settings["frequencies"]["pin"]

    ####################################

    # PUB METHODS
    def attach(self, subscriber):
        self.__subscribers.append(subscriber)

    def detach(self):
        self.__subscribers.pop()

    def get_subscribers(self):
        return [type(x).__name__ for x in self.__subscribers]

    def update_subscribers(self):
        for sub in self.__subscribers:
            sub.update()

    def add_content(self, content):
        self.__content = content

    def get_content(self):
        return self.__content

    def publish(self, data):
        self.add_content(data)
        self.update_subscribers()

    # END PUB METHODS

    def connect_mqtt(self):
        self.broker = MqttBroker()
        self.broker.connect_mqtt()
        self.broker.client.loop_start()

    def run(self):
        self.db.replace_web_control_value(False)
        self.ledData.fade = True
        self.ledData.all_on = True
        print("start checking commands")
        self.turn_off_amplifier()
        while True:
            if not self.db.get_web_control_value():
                self.check_radio_on_off()
                self.check_shutdown_raspi()
                self.check_change_speakers()
                self.check_radio_lock()
                self.check_poti_change()
                if not self.radio_lock:
                    changed_hardware = self.get_changed_buttons()
                    changed_hardware.extend(self.get_frequency_change())
                    if changed_hardware:
                        self.process_hardware_change(changed_hardware)
            else:
                print("web control")
                self.check_radio_on_off()
                changed_hardware = self.get_command_changed()
                self.get_command_from_db()
                print(f"changed: {changed_hardware}")
                if changed_hardware:
                    if "volume" in changed_hardware:
                        self.send_volume(self.current_command["volume"])
                    self.process_hardware_value_change()
                    self.old_command = self.current_command
            time.sleep(1)

    def get_command_changed(self):
        changed_hardware = []
        if self.current_command["buttonOnOff"] != self.db.get_button_on_off():
            changed_hardware.append("buttonOnOff")
        if self.current_command["buttonLang"] != self.db.get_button_lang():
            changed_hardware.append("buttonLang")
        if self.current_command["buttonMittel"] != self.db.get_button_mittel():
            changed_hardware.append("buttonMittel")
        if self.current_command["buttonKurz"] != self.db.get_button_kurz():
            changed_hardware.append("buttonKurz")
        if self.current_command["buttonUKW"] != self.db.get_button_ukw():
            changed_hardware.append("buttonUKW")
        if self.current_command["buttonTa"] != self.db.get_button_ukw():
            changed_hardware.append("buttonTa")
        if self.current_command["buttonSprMus"] != self.db.get_button_spr_mus():
            changed_hardware.append("buttonSprMus")
        if self.current_command["volume"] != self.db.get_volume():
            changed_hardware.append("volume")
        if self.current_command["posLangKurzMittel"] != self.db.get_pos_lang_mittel_kurz():
            changed_hardware.append("posLangKurzMittel")
        if self.current_command["posUKW"] != self.db.get_pos_ukw():
            changed_hardware.append("posUKW")
        return changed_hardware

    def get_command_from_db(self):
        self.current_command["buttonOnOff"] = self.db.get_button_on_off()
        self.current_command["buttonLang"] = self.db.get_button_lang()
        self.current_command["buttonMittel"] = self.db.get_button_mittel()
        self.current_command["buttonKurz"] = self.db.get_button_kurz()
        self.current_command["buttonUKW"] = self.db.get_button_ukw()
        self.current_command["buttonSprMus"] = self.db.get_button_spr_mus()
        self.current_command["buttonTa"] = self.db.get_button_ta()
        self.current_command["volume"] = self.db.get_poti_value_web()
        self.current_command["bass"] = self.db.get_bass_value_web()
        self.current_command["treble"] = self.db.get_treble_value_web()
        self.current_command["posLangKurzMittel"] = self.db.get_pos_lang_mittel_kurz()
        self.current_command["posUKW"] = self.db.get_pos_ukw()

    def check_shutdown_raspi(self):
        if self.db.get_shutdown():
            self.ledStrip.raspi_off = True
            time.sleep(4)
            self.raspberry.turn_raspi_off()

    def check_radio_lock(self):
        if self.radio_buttons.button_spr.is_click():
            self.radio_lock = not self.radio_lock
            print(f"radio lock changed: {self.radio_lock}")

    def check_radio_on_off(self):
        if self.settings["buttons"]["on_off"]["active"]:
            if self.radio_buttons.button_on_off.is_click() and not self.db.get_web_control_value():
                self.on = not self.on
                if self.on:
                    self.turn_on_radio()
                else:
                    self.turn_off_radio()
            elif self.db.get_web_control_value() and self.db.get_button_on_off():
                self.on = True
            elif self.db.get_web_control_value() and not self.db.get_button_on_off():
                self.on = False
        else:
            self.on = True
            self.turn_on_radio(debug=False)

    def check_change_speakers(self):
        if self.radio_buttons.button_on_off.double_click():
            self.speakers.change_once()
            if not self.speakers.play_radio:
                self.publish("stop")
            if self.mqtt:
                if not self.speakers.play_central:
                    self.broker.publish_start_stop("0")

    def process_hardware_change(self, changed_hardware_list):
        # TODO: only set volume. rest is handled by process hardware value change
        # mehtod can be deleted and set volume and change hardware
        for changed_hardware in changed_hardware_list:
            if changed_hardware in ["posLangKurzMittel", "posUKW"]:
                pass
                # print("------------------------------------")
                # print(f"encoder changed {self.current_command['posLangKurzMittel']}, ")
                #      f"{self.current_command['posUKW']}")
            self.process_hardware_value_change()

    @staticmethod
    def turn_off_amplifier():
        print("TURN OFF")
        GPIO.output(4, False)

    @staticmethod
    def turn_on_amplifier():
        print("Turn ON")
        GPIO.output(4, True)

    def turn_on_radio(self, debug: bool = True):
        self.ledStrip.radio_off = False
        if debug:
            print("Turning on Radio")
        radio_frequency, encoder_value = self.get_button_frequency()
        if radio_frequency and self.on:
            stream = self.get_frequency_stream(radio_frequency, encoder_value)
            if debug:
                print("stream: ", stream)
            if stream:
                if self.current_stream.radio_url != stream.radio_url:
                    self.start_stream(stream)
        else:
            if debug:
                print("No button pressed. Playing nothing")

    def turn_off_radio(self):
        self.ledStrip.radio_off = True
        self.ledStrip.off_button_on = False
        print("Turning off radio")
        if self.speakers.play_radio:
            self.publish("stop")
        self.turn_off_amplifier()
        self.current_stream.radio_url = None
        if self.mqtt:
            if self.speakers.play_central:
                self.broker.publish_start_stop("0")

    def start_stream(self, stream: RadioFrequency):
        print(f"Playing stream: {stream}")
        self.turn_on_amplifier()
        if self.speakers.play_radio:
            self.publish(stream)
        self.db.replace_stream(stream.radio_url)
        self.db.replace_radio_name(stream.name + "; " + stream.radio_name)
        self.current_stream = stream
        self.playing = True
        if self.mqtt:
            if self.speakers.play_central:
                self.broker.publish_start_stop("1")
                self.broker.publish_stream(stream.radio_url)

    @staticmethod
    def get_frequency_stream(button_frequencies, encoder_value):
        for radio_frequency in button_frequencies.frequencies:
            try:
                if radio_frequency.minimum <= encoder_value < radio_frequency.maximum:
                    return radio_frequency
            except TypeError:
                return None
        return None

    def get_button_frequency(self):
        # TODO: do i need change button change, when here button state is retrieved again
        if not self.db.get_web_control_value():
            if self.radio_buttons.button_lang.state:
                return LangFrequencies(), self.current_command["posLangKurzMittel"]
            elif self.radio_buttons.button_mittel.state:
                return MittelFrequencies(), self.current_command["posLangKurzMittel"]
            elif self.radio_buttons.button_kurz.state:
                return KurzFrequencies(), self.current_command["posLangKurzMittel"]
            elif self.radio_buttons.button_ukw.state:
                return UKWFrequencies(), self.current_command["posLangKurzMittel"] # self.current_command["posUKW"]
            elif self.radio_buttons.button_ta.state:
                return TaFrequencies(), self.current_command["posLangKurzMittel"]
            # elif self.radio_buttons.button_spr.state:
            #     return SprFrequencies(), self.current_command["posUKW"]
            else:
                # print("using NONE")
                return None, None
        else:
            if self.db.get_button_lang():
                return LangFrequencies(), self.current_command["posLangKurzMittel"]
            elif self.db.get_button_mittel():
                return MittelFrequencies(), self.current_command["posLangKurzMittel"]
            elif self.db.get_button_kurz():
                return KurzFrequencies(), self.current_command["posLangKurzMittel"]
            elif self.db.get_button_ta():
                return TaFrequencies(), self.current_command["posLangKurzMittel"]
            elif self.db.get_button_ukw():
                return UKWFrequencies(), self.current_command["posUKW"]
            elif self.db.get_button_spr_mus():
                return SprFrequencies(), self.current_command["posUKW"]
            else:
                # print("using NONE")
                return None, None

    def set_volume(self, volume):
        if 1250 < volume < 1400:
            # somehow after 24000 poti switches to 1250 till 1350
            volume = self.volume_old
        else:
            volume = int(-(volume - self.volume_min) / (self.volume_min - self.volume_max) * 100)
        if volume < 0:
            volume = 0
        elif volume > 100:
            volume = 100
        self.volume_old = volume
        self.db.replace_volume(volume)
        self.send_volume(volume)

    def set_treble(self, treble):
        treble = -(int(-(self.treble_max - treble) / (self.treble_min - self.treble_max) * 40) - 20)
        if treble < -20:
            treble = -20
        elif treble > 20:
            treble = 20
        self.db.replace_treble(treble)
        self.send_treble(treble)

    def set_bass(self, bass):
        bass = int(-(bass - self.bass_min) / (self.bass_min - self.bass_max) * 40) - 20
        if bass < 0:
            bass = 0
        elif bass > 100:
            bass = 100
        self.db.replace_bass(bass)
        self.send_bass(bass)

    def send_volume(self, volume):
        if self.speakers.play_radio:
            self.publish(f"volume:{volume}")
        if self.mqtt:
            if self.speakers.play_central:
                self.broker.publish_volume(volume)

    def send_bass(self, bass):
        if self.speakers.play_radio:
            self.publish(f"bass:{bass}")
        if self.mqtt:
            if self.speakers.play_central:
                self.broker.publish_volume(bass)

    def send_treble(self, treble):
        if self.speakers.play_radio:
            self.publish(f"treble:{treble}")
        if self.mqtt:
            if self.speakers.play_central:
                self.broker.publish_treble(treble)

    def get_frequency_change(self):
        changed_hardware = []
        value = self.db.get_ads_pin_value(self.pin_frequencies)
        if value != self.old_command["posLangKurzMittel"]:
            changed_hardware.append("posLangKurzMittel")
            self.current_command["posLangKurzMittel"] = value
        return changed_hardware

    def check_poti_change(self):
        if self.volume_on:
            value = self.db.get_ads_pin_value(self.pin_volume)
            if value != self.old_command["volume"]:
                self.current_command["volume"] = value
                self.set_volume(value)

        if self.bass_on:
            value = self.db.get_ads_pin_value(self.pin_bass)
            if value != self.old_command["bass"]:
                self.current_command["bass"] = value
                self.set_bass(value)

        if self.treble_on:
            value = self.db.get_ads_pin_value(self.pin_treble)
            if value != self.old_command["treble"]:
                self.current_command["treble"] = value
                self.set_treble(value)

    def get_changed_buttons(self):
        self.radio_buttons.set_value()
        changed_hardware = []
        state = self.radio_buttons.button_on_off.state
        if self.current_command["buttonOnOff"] != state:
            self.ledData.on_button_on = state
            self.ledData.off_button_on = not state
            print(f"BUTTON ON OFF CHANGED {state}")
            self.current_command["buttonOnOff"] = state
            changed_hardware.append("buttonOnOff")
        state = self.radio_buttons.button_lang.state
        if self.current_command["buttonLang"] != state:
            self.ledData.on_button_lang = state
            self.ledData.off_button_lang = not state
            print(f"BUTTON LANG CHANGED: {state}")
            self.current_command["buttonLang"] = state
            changed_hardware.append("buttonLang")
        state = self.radio_buttons.button_mittel.state
        if self.current_command["buttonMittel"] != state:
            self.ledData.on_button_mittel = state
            self.ledData.off_button_mittel = not state
            print(f"BUTTON MITTEL CHANGED: {state}")
            self.current_command["buttonMittel"] = state
            changed_hardware.append("buttonMittel")
        state = self.radio_buttons.button_kurz.state
        if self.current_command["buttonKurz"] != state:
            self.ledData.on_button_kurz = state
            self.ledData.off_button_kurz = not state
            print(f"BUTTON KURZ CHANGED: {state}")
            self.current_command["buttonKurz"] = state
            changed_hardware.append("buttonKurz")
        state = self.radio_buttons.button_ukw.state
        if self.current_command["buttonUKW"] != state:
            self.ledData.on_button_ukw = state
            self.ledData.off_button_ukw = not state
            print(f"BUTTON UKW CHANGED: {state}")
            self.current_command["buttonUKW"] = state
            changed_hardware.append("buttonUKW")

        state = self.radio_buttons.button_spr.state
        if self.current_command["buttonSprMus"] != state:
            self.ledData.on_button_spr = state
            self.ledData.off_button_spr = not state
            print(f"BUTTON SPR CHANGED: {state}")
            self.current_command["buttonSprMus"] = state
            changed_hardware.append("buttonSprMus")
        state = self.radio_buttons.button_ta.state
        if self.current_command["buttonUKW"] != state:
            # TODO: led
            self.ledData.on_button_ukw = state
            self.ledData.off_button_ukw = not state
            print(f"BUTTON TA CHANGED: {state}")
            self.current_command["buttonTa"] = state
            changed_hardware.append("buttonUKW")
        return changed_hardware

    def process_hardware_value_change(self):
        radio_frequency, encoder_value = self.get_button_frequency()
        print(f"radio_frequency {radio_frequency} and {self.on} : encoder value: {encoder_value}")
        if not radio_frequency:
            if self.playing:
                if self.speakers.play_radio:
                    self.publish("stop")
                self.playing = False
        elif radio_frequency and self.on:
            stream = self.get_frequency_stream(radio_frequency, encoder_value)
            if stream:
                if self.current_stream.radio_url != stream.radio_url:
                    print("Changing stream")
                    if self.playing:
                        if self.speakers.play_radio:
                            self.publish("stop")
                        self.playing = False
                    if radio_frequency:
                        print(f"Playing playlist: {stream}")
                        self.db.replace_stream(stream.radio_url)
                        self.db.replace_radio_name(stream.name + "; " + stream.radio_name)
                        self.turn_on_amplifier()
                        if self.speakers.play_radio:
                            self.publish(stream)
                        self.playing = True
                        self.current_stream = stream
                        if self.mqtt:
                            if self.speakers.play_central:
                                self.broker.publish_start_stop("1")
                                self.broker.publish_stream(stream.radio_url)

    def stop_player(self):
        if self.speakers.play_radio:
            self.publish("stop")
        # global_.stop = True
        self.current_stream.radio_url = None
        if self.mqtt:
            if self.speakers.play_central:
                self.broker.publish_start_stop("0")

    def error(self):
        # save error cause
        # light up red lamp
        pass


if __name__ == "__main__":
    radio = Radio()
    radio.run()
