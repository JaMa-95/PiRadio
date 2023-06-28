import datetime
from dataclasses import dataclass
import RPi.GPIO as GPIO
from db.db import Database


class ButtonRaspi:
    def __init__(self, button_number: int = 0, reversed_: bool = False, long_click_threshold: int = 50):
        # BCM-Nummerierung verwenden
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(button_number, GPIO.OUT)
        self.button_number = button_number
        self.value: int = 99
        self.value_old: int = 0
        self.value_olds = []
        self.value_old_index = 0
        self.indexer = 0

        self.reversed = reversed_

        self.long_threshold: int = long_click_threshold

        self.last_click: list = [None, None]
        self.last_click_index: int = 0

        self.is_clicked: bool = False
        self.on_off_wait: bool = False

        self.state = False

    def is_click(self):
        # TODO: check if indexer needed
        if not self.on_off_wait and self.indexer > 5:
            self.on_off_wait = True
            self.state = GPIO.input(self.button_number)
            self.set_is_clicked()
            return True
        return False

    def double_click(self):
        if self.last_click[0] and self.last_click[1]:
            time_delta_a = self.last_click[0] - self.last_click[1]
            time_delta_b = self.last_click[1] - self.last_click[0]
            if time_delta_a.seconds < 2 or time_delta_b.seconds < 2:
                self.reset_double_click()
                return True
        return False

    def reset_double_click(self):
        self.last_click[0] = None
        self.last_click[1] = None

    def long_click(self):
        if self.indexer > self.long_threshold:
            return True
        return False

    def get_value(self):
        return self.value

    def set_value(self):
        """
        :return: True if changed
        """
        self.state = GPIO.input(self.button_number)
        if self.reversed:
            self.state = not self.state
        self.value_olds.append(self.state)
        self.value_old = self.value
        self.value = self.state
        if self.state:
            self.is_clicked = True
            self.indexer += 1
            return True
        else:
            self.on_off_wait = False
            self.is_clicked = False
            self.indexer = 0
            return True

    def get_last_clicked_index(self):
        self.last_click_index = (self.last_click_index + 1) % 2
        return self.last_click_index

    def set_is_clicked(self):
        self.last_click[self.get_last_clicked_index()] = datetime.datetime.now()


@dataclass
class RadioButtonsRaspi:
    button_on_off: ButtonRaspi = ButtonRaspi(0, True)
    button_lang: ButtonRaspi = ButtonRaspi(24)
    button_mittel: ButtonRaspi = ButtonRaspi(25)
    button_kurz: ButtonRaspi = ButtonRaspi(9)
    button_ukw: ButtonRaspi = ButtonRaspi(7)
    button_spr: ButtonRaspi = ButtonRaspi(8)
    button_ta: ButtonRaspi = ButtonRaspi(23, True)

    db = Database()

    def set_values_to_db(self):
        self.set_value()
        self.db.replace_button_ukw(self.button_ukw.state)
        self.db.replace_button_spr_mus(self.button_spr.state)
        self.db.replace_button_kurz(self.button_kurz.state)
        self.db.replace_button_mittel(self.button_mittel.state)
        self.db.replace_button_lang(self.button_lang.state)
        self.db.replace_button_on_off(self.button_on_off.state)
        self.db.replace_button_ta(self.button_ta.state)

    def set_value(self):
        self.button_on_off.set_value()
        self.button_lang.set_value()
        self.button_mittel.set_value()
        self.button_kurz.set_value()
        self.button_ukw.set_value()
        self.button_spr.set_value()
        self.button_ta.set_value()
        return True

    def get_pressed_button(self):
        self.set_value()
        state_on = self.button_on_off.state
        if state_on:
            state = self.button_lang.state
            if state:
                return "buttonLang"
            state = self.button_mittel.state
            if state:
                return "buttonMittel"
            state = self.button_kurz.state
            if state:
                return "buttonKurz"
            state = self.button_ukw.state
            if state:
                return "buttonUKW"
            state = self.button_spr.state
            if state:
                return "buttonSprMus"
            state = self.button_ta.state
            if state:
                return "buttonTa"
