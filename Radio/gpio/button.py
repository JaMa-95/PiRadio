import datetime
import json
from dataclasses import dataclass
from typing import List
import RPi.GPIO as GPIO

from Radio.db.db import Database
from Radio.radioFrequency import Frequencies
from Radio.util.util import get_project_root


class ButtonRaspi:
    def __init__(self, name: str = ""):
        self.name: str = name
        self.pin: int = 0
        self.active: bool = False
        self.reversed: bool = False
        self.frequency_pos: str = ""
        self.frequency_list: Frequencies = None
        self.is_frequency_lock: bool = False
        self.is_on_off_button: bool = False

        self.cycle_time: float = 0.0

        self.value: int = 99
        self.value_old: int = 0
        self.value_olds = []
        self.value_old_index = 0
        self.indexer = 0

        self.long_threshold: int = 50

        self.last_click: list = [None, None]
        self.last_click_index: int = 0

        self.is_clicked: bool = False
        self.on_off_wait: bool = False

        self.state = False

        self.load_from_settings()
        self.setup_pin()

    def load_from_settings(self):
        path_settings = get_project_root() / 'data/settings.json'
        with open(path_settings.resolve()) as f:
            settings = json.load(f)
        if settings["buttons"][self.name]["active"]:
            self.pin = settings["buttons"][self.name]["pin"]
            self.reversed = settings["buttons"][self.name]["reversed"]
            self.active = settings["buttons"][self.name]["active"]
            self.frequency_pos = settings["buttons"][self.name]["frequency"]["pos"]
            self.frequency_list = Frequencies(settings["buttons"][self.name]["frequency"]["musicList"])
            self.is_on_off_button = settings["buttons"][self.name]["is_on_off"]
            self.is_frequency_lock = settings["buttons"][self.name]["is_frequency_lock"]

    def setup_pin(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

    def set_pin(self, pin: int):
        GPIO.setup(self.pin, GPIO.IN)
        GPIO.setup(pin, GPIO.OUT)
        self.pin = pin

    def set_reversed(self, reversed_: bool = False):
        self.reversed = reversed_

    def is_click(self):
        # TODO: measure is click with time
        if not self.on_off_wait and self.indexer > 5:
            self.on_off_wait = True
            self.state = GPIO.input(self.pin)
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
        self.state = GPIO.input(self.pin)
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
    on_off_button: ButtonRaspi = None
    frequency_lock_buttons: List[ButtonRaspi] = None
    buttons: List[ButtonRaspi] = None

    db = Database()

    def __post_init__(self):
        path_settings = get_project_root() / 'data/settings.json'
        with open(path_settings.resolve()) as f:
            settings = json.load(f)
        if self.buttons is None:
            self.buttons = []
        for name, button_settings in settings["buttons"].items():
            if button_settings["is_on_off"]:
                self.on_off_button = ButtonRaspi(name)
            elif button_settings["is_frequency_lock"]:
                self.frequency_lock_buttons.append(ButtonRaspi(name))
            else:
                self.buttons.append(ButtonRaspi(name))

    def set_values_to_db(self):
        self.set_value()
        for button in self.buttons:
            self.db.replace_button(name=button.name,
                                   value=button.state)

    def set_value(self):
        for button in self.buttons:
            button.set_value()
        return True

    def get_pressed_button(self):
        self.set_value()
        if self.button_on_off.state:
            for button in self.buttons:
                if button.state:
                    return f"button{button.name}"
