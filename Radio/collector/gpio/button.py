import json
from collections import deque
from typing import List

from Radio.util.radioExceptions import SystemNotSupported
from Radio.util.util import is_raspberry

if is_raspberry():
    IS_RASPBERRY_PI = True
    import RPi.GPIO as GPIO
else:
    IS_RASPBERRY_PI = False

from Radio.db.db import Database
from Radio.dataProcessing.radioFrequency import Frequencies
from Radio.util.util import get_project_root
from Radio.util.singleton import Singleton
from Radio.util.sensorMsg import ButtonsData, ButtonState


class ButtonRaspi:
    def __init__(self, name: str = "", is_on_off: bool = False, is_frequency_lock: bool = False,
                 is_change_speaker: bool = False, is_on_off_raspi: bool = False, mock: bool = False):
        self.name: str = name
        self.pin: int = 0
        self.active: bool = False
        self.reversed: bool = False
        self.frequency_pos: str = ""
        self.frequency_list: Frequencies = None
        self.is_frequency_lock: bool = is_frequency_lock
        self.is_on_off_button: bool = is_on_off
        self.is_change_speaker: bool = is_change_speaker
        self.is_on_off_raspi: bool = is_on_off_raspi
        self.mock: bool = mock

        self.state = False

        self.max_values: int = 10
        # shows last x states
        self.states = deque([False] * self.max_values)

        if self.name:
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
            if settings["buttons"][self.name]["frequency"]["musicList"]:
                self.frequency_list = Frequencies(settings["buttons"][self.name]["frequency"]["musicList"])
            # self.is_on_off_button = settings["buttons"][self.name]["is_on_off"]
            if "is_frequency_lock" in settings["buttons"][self.name]:
                self.is_frequency_lock = settings["buttons"][self.name]["is_frequency_lock"]

    def setup_pin(self):
        if not IS_RASPBERRY_PI and not self.mock:
            raise SystemNotSupported("Not a raspberry pi or unsupported version")
        if not self.mock:
            GPIO.setmode(GPIO.BCM)
            # TODO: give PUD up mode
            if self.is_on_off_raspi:
                print(f"raspi init: {self.pin}")
                GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            else:
                GPIO.setup(self.pin, GPIO.OUT)

    def set_pin(self, pin: int):
        GPIO.setup(self.pin, GPIO.IN)
        GPIO.setup(pin, GPIO.OUT)
        self.pin = pin

    def set_reversed(self, reversed_: bool = False):
        self.reversed = reversed_

    def get_value(self):
        return self.value

    def _put_state_to_list(self, value):
        self.states.rotate(1)
        self.states[0] = value

    def set_value(self):
        """
        :return: True if changed
        """
        if not self.mock:
            self.state = GPIO.input(self.pin)
            if self.reversed:
                self.state = not self.state
            self._put_state_to_list(self.state)
        else:
            if self.pin == 24 or self.pin == 4:
                self.state = True
            else:
                self.state = False
            self._put_state_to_list(self.state)


class RadioButtonsRaspi(Singleton):

    def __init__(self, mock: bool = False, debug: bool = False):
        if self._Singleton__initialized:
            return
        self.mock = mock
        self.debug: bool = debug
        self.on_off_button: ButtonRaspi = ButtonRaspi(mock=mock)
        self.on_off_raspi_button: ButtonRaspi = ButtonRaspi(mock=mock)
        self.change_speaker_button: ButtonRaspi = ButtonRaspi(mock=mock)
        self.radio_lock_button: ButtonRaspi = ButtonRaspi(mock=mock)
        self.frequency_lock_button: ButtonRaspi = ButtonRaspi(mock=mock)
        self.buttons: List[ButtonRaspi] = None

        self.db = Database()
        self._init_settings()

    def _init_settings(self):
        path_settings = get_project_root() / 'data/settings.json'
        with open(path_settings.resolve()) as f:
            settings = json.load(f)
        if self.buttons is None:
            self.buttons = []
        for name, button_settings in settings["buttons"].items():
            if "is_on_off" in button_settings:
                self.on_off_button = ButtonRaspi(name, is_on_off=True, mock=self.mock)
            elif "is_on_off_raspi" in button_settings:
                self.on_off_raspi_button = ButtonRaspi(name, is_on_off_raspi=True, mock=self.mock)
            elif "is_frequency_lock" in button_settings:
                self.frequency_lock_button = ButtonRaspi(name, is_frequency_lock=True, mock=self.mock)
            elif "is_change_speaker" in button_settings:
                self.change_speaker_button = ButtonRaspi(name, is_change_speaker=True, mock=self.mock)
            else:
                self.buttons.append(ButtonRaspi(name, mock=self.mock))

    def set_values(self):
        for button in self.buttons:
            button.set_value()
        if self.frequency_lock_button.active:
            self.frequency_lock_button.set_value()
        if self.change_speaker_button.active:
            self.change_speaker_button.set_value()
        if self.on_off_button.active:
            self.on_off_button.set_value()
        if self.on_off_raspi_button.active:
            self.on_off_raspi_button.set_value()
        return True

    def get_values(self) -> ButtonsData:
        self.set_values()
        data = ButtonsData()
        for button in self.buttons:
            data.add_value(ButtonState(button.pin, button.state, button.states))
        if self.frequency_lock_button.active:
            data.add_value(ButtonState(self.frequency_lock_button.pin,
                                       self.frequency_lock_button.state,
                                       self.frequency_lock_button.states))
        if self.change_speaker_button.active:
            data.add_value(ButtonState(self.change_speaker_button.pin,
                                       self.change_speaker_button.state,
                                       self.change_speaker_button.states))
        if self.on_off_button.active:
            data.add_value(ButtonState(self.on_off_button.pin,
                                       self.on_off_button.state,
                                       self.on_off_button.states))
        if self.on_off_raspi_button.active:
            data.add_value(ButtonState(self.on_off_raspi_button.pin,
                                       self.on_off_raspi_button.state,
                                       self.on_off_raspi_button.states))
        return data
