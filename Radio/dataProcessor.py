import json
import time

from Radio.RadioAction import RadioAction, ButtonClickStates
from Radio.db.db import Database
from Radio.sensorMsg import SensorMsg, ButtonsData, AnalogData, ButtonState
from Radio.util.DataTransmitter import DataTransmitter
from Radio.util.util import get_project_root


class DataProcessor:
    def __init__(self):
        self.data_transmitter: DataTransmitter = DataTransmitter()

        self.button_processor: ButtonProcessor = ButtonProcessor()
        self.analog_processor: AnalogProcessor = AnalogProcessor(self.publish)

        self.current_data: SensorMsg = SensorMsg()

        self.__subscribers = []
        self.__content = None

        self.cycle_time: float = 0.0

        self.pin_frequencies: int = 0
        self.pin_volume: int = 0
        self.pin_bass: int = 0
        self.pin_treble: int = 0

        self.settings: dict = {}
        self.load_settings()

    def load_settings(self):
        with open(get_project_root() / 'data/settings.json') as f:
            self.settings = json.load(f)

        self.cycle_time = self.settings["cycle_time"]

        # self.amplifier_switch_pin = self.settings["amplifier_pin"]
        # GPIO.setup(self.amplifier_switch_pin, GPIO.OUT)

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

    def run(self):
        while True:
            # TODO: wait instead of endless loop
            if self.data_transmitter.has_data():
                data: SensorMsg = self.data_transmitter.receive()
                self.process_buttons(data.buttons_data)
                self.process_analogs(data.analog_data)
            else:
                time.sleep(self.cycle_time)

    def process_buttons(self, buttons_data: ButtonsData):
        self.current_data.buttons_data = buttons_data
        self.button_processor.process(buttons_data)

    def process_analogs(self, analog_data: AnalogData):
        if analog_data.is_empty():
            return None
        if self.current_data.analog_data.get_data() == analog_data:
            return None
        self.current_data.analog_data = analog_data
        self.analog_processor.process(analog_data)


class ButtonProcessData:
    def __init__(self, pin):
        self.pin = pin
        self.data: ButtonState = ButtonState(pin=self.pin, state=False, states=[])
        self.short_threshold: int = 2
        self.long_threshold: int = 10
        self.button_happening: RadioAction = RadioAction()

    def process_data(self):
        if self.data.state:
            self.button_happening.execute(ButtonClickStates.BUTTON_STATE_ON)
        else:
            self.button_happening.execute(ButtonClickStates.BUTTON_STATE_OFF)
        if self.is_short_click():
            self.button_happening.execute(ButtonClickStates.BUTTON_STATE_SHORT_CLICK)
        elif self.is_long_click():
            self.button_happening.execute(ButtonClickStates.BUTTON_STATE_LONG_CLICK)
        elif self.is_double_click():
            self.button_happening.execute(ButtonClickStates.BUTTON_STATE_DOUBLE_CLICK)

    def _is_click(self, threshold: int):
        # TODO: measure is click with time
        counter = 0
        for value in self.data.states():
            if value is True:
                counter += 1
                if counter > threshold:
                    return True
            else:
                return False
        return False

    def is_short_click(self):
        return self._is_click(self.short_threshold)

    def is_long_click(self):
        return self._is_click(self.long_threshold)

    def is_double_click(self):
        # TODO
        raise NotImplemented


class ButtonProcessor:
    def __init__(self):
        self.buttons: dict = {}
        self._load_settings()

    def _load_settings(self):
        path_settings = get_project_root() / 'data/settings.json'
        with open(path_settings.resolve()) as f:
            settings = json.load(f)

        for name, button_settings in settings["buttons"].items():
            if button_settings["active"]:
                self.buttons[name] = ButtonProcessData(button_settings["pin"])

    def process(self, buttons_data: ButtonsData):
        for button in buttons_data.get_data():
            self._check_button(button)

    def _check_button(self, data):
        pass


class AnalogProcessor:
    def __init__(self, publish_function):
        self.publish_function = publish_function

        self.db: Database = Database()

        self.volume_old: int = 0
        self.volume_min: int = 0
        self.volume_max: int = 0
        self.volume_on: bool = False

        self.bass_min: int = 0
        self.bass_max: int = 0
        self.bass_on: bool = False
        self.bass_old: int = 0

        self.treble_min: int = 0
        self.treble_max: int = 0
        self.treble_on: bool = False
        self.treble_old: int = 0

        self.pin_frequencies: int = 0
        self.pin_volume: int = 0
        self.pin_bass: int = 0
        self.pin_treble: int = 0

        self.settings = {}
        self.load_settings()

    def load_settings(self):
        with open(get_project_root() / 'data/settings.json') as f:
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
        # TODO: mutliple frequencies waht now?
        self.pin_frequencies = self.settings["frequencies"]["posLangKurzMittel"]["pin"]

    def process(self, data: AnalogData):
        for analog in data.get_data():
            if analog.pin == self.pin_volume:
                self.set_volume(analog.value)
            elif analog.pin == self.pin_bass:
                self.set_bass(analog.value)
            elif analog.pin == self.pin_treble:
                self.set_treble(analog.value)

    def set_volume(self, volume):
        volume = int(-(volume - self.volume_min) / (self.volume_min - self.volume_max) * 100)
        if volume < 0:
            volume = 0
        elif volume > 100:
            volume = 100
        if volume == self.volume_old:
            return
        # print(f"Volume: {volume}")
        self.volume_old = volume
        self.db.replace_volume(volume)
        self.publish_function(f"volume:{volume}")

    def set_bass(self, bass):
        bass = int(-(bass - self.bass_min) / (self.bass_min - self.bass_max) * 40) - 20
        if bass < 0:
            bass = 0
        elif bass > 100:
            bass = 100
        if bass == self.bass_old:
            return
        self.bass_old = bass
        self.db.replace_bass(bass)
        self.publish_function(f"bass:{bass}")

    def set_treble(self, treble):
        treble = -(int(-(self.treble_max - treble) / (self.treble_min - self.treble_max) * 40) - 20)
        if treble < -20:
            treble = -20
        elif treble > 20:
            treble = 20
        if treble == self.treble_old:
            return
        self.treble_old = treble
        self.db.replace_treble(treble)
        self.publish_function(f"treble:{treble}")
