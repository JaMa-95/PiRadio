import json
import time
from typing import List

from Radio.RadioAction import RadioAction, ButtonClickStates, Actions
from Radio.db.db import Database
from Radio.sensorMsg import SensorMsg, ButtonsData, AnalogData, ButtonState
from Radio.util.DataTransmitter import DataTransmitter
from Radio.util.util import get_project_root
from Radio.radioFrequency import Frequencies, RadioFrequency


class DataProcessor:
    def __init__(self):
        self.data_transmitter: DataTransmitter = DataTransmitter()

        self.button_processor: ButtonProcessor = ButtonProcessor()
        self.analog_processor: AnalogProcessor = AnalogProcessor(self.publish)

        self.sensor_msg_old: SensorMsg = SensorMsg()
        self.active_actions: Actions = Actions()

        self.__subscribers = []
        self.__content = None

        self.cycle_time: float = 0.0

        self.pin_frequencies: int = 0
        self.pin_volume: int = 0
        self.pin_bass: int = 0
        self.pin_treble: int = 0

        self.settings: dict = {}
        self.load_settings()

        self.db: Database = Database()

    # TODO: extra publisher class
    def load_settings(self):
        with open(get_project_root() / 'data/settings.json') as f:
            self.settings = json.load(f)

        self.cycle_time = self.settings["cycle_time"]

        # self.amplifier_switch_pin = self.settings["amplifier_pin"]
        # GPIO.setup(self.amplifier_switch_pin, GPIO.OUT)

    # TODO: implement this as reference class
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

    def run(self):
        while True:
            # TODO: wait instead of endless loop
            if self.data_transmitter.has_data():
                sensor_msg_current: SensorMsg = self.data_transmitter.receive()
                sensor_msg_current = self.active_actions.process(sensor_msg_current=sensor_msg_current,
                                                                 sensor_msg_old=self.sensor_msg_old)
                self.process_analogs(sensor_msg_current.analog_data)
                self.process_buttons(sensor_msg_current.buttons_data)
                self.sensor_msg_old = sensor_msg_current
            else:
                time.sleep(self.cycle_time)

    # mostly for testing purpose
    def add_remove_actions(self, action: RadioAction):
        self.active_actions.add_or_remove_action(action)

    def process_buttons(self, buttons_data: ButtonsData):
        self.button_processor.process(buttons_data)

    def process_analogs(self, analog_data: AnalogData):
        if analog_data.is_empty():
            return None
        if self.sensor_msg_old.analog_data.get_data_sensor() == analog_data:
            return None
        self.analog_processor.process(analog_data, self.active_actions)


class ButtonStatus:
    def __init__(self, name: str, pin: int, frequency_list: Frequencies):
        self.name: str = name
        self.pin: int = pin
        self.frequency_list: Frequencies = frequency_list
        self.status: bool = False


class ButtonProcessData:
    def __init__(self, name: str, pin: int, apply_state: ButtonClickStates, frequency_list: Frequencies):
        self.name = name
        self.pin = pin
        self.state: ButtonState = ButtonState(pin=self.pin, state=False, states=[])
        self.short_threshold: int = 2
        self.long_threshold: int = 10
        self.button_happening: RadioAction = RadioAction(apply_state)
        self.frequency_list: Frequencies = frequency_list

    def process_data(self, sensor_msg_new: SensorMsg, sensor_msg_old: SensorMsg) -> SensorMsg:
        sensor_msg_updated = None
        if self.state.state:
            sensor_msg_updated = self.button_happening.check_and_execute(ButtonClickStates.BUTTON_STATE_ON,
                                                                         sensor_msg_new,
                                                                         sensor_msg_old)
        else:
            sensor_msg_updated = self.button_happening.check_and_execute(ButtonClickStates.BUTTON_STATE_OFF,
                                                                         sensor_msg_new,
                                                                         sensor_msg_old)
        if self.is_short_click():
            return self.button_happening.check_and_execute(ButtonClickStates.BUTTON_STATE_SHORT_CLICK,
                                                           sensor_msg_updated,
                                                           sensor_msg_old)
        elif self.is_long_click():
            return self.button_happening.check_and_execute(ButtonClickStates.BUTTON_STATE_LONG_CLICK,
                                                           sensor_msg_updated,
                                                           sensor_msg_old)
        elif self.is_double_click():
            return self.button_happening.check_and_execute(ButtonClickStates.BUTTON_STATE_DOUBLE_CLICK,
                                                           sensor_msg_updated,
                                                           sensor_msg_old)

    # TODO: Test this with min max
    def get_frequency_stream(self, sensor_value: int) -> None | RadioFrequency:
        over_min_max_frequency = None
        for index, radio_frequency in enumerate(self.frequency_list.frequencies):
            try:
                if radio_frequency.minimum <= sensor_value < radio_frequency.maximum:
                    return radio_frequency
                elif index == 0 and sensor_value < radio_frequency.minimum:
                    over_min_max_frequency = radio_frequency
                elif index == len(self.frequency_list.frequencies) and sensor_value > radio_frequency.maximum:
                    over_min_max_frequency = radio_frequency
            except TypeError:
                return None
        return over_min_max_frequency

    def _is_click(self, threshold: int):
        # TODO: measure is click with time
        counter = 0
        for value in self.state.states():
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


class AnalogProcessData:
    def __init__(self, pin: int, name: str, is_frequency: bool, frequencies: Frequencies):
        self.name: str = name
        self.pin: int = pin
        self.is_frequency: bool = is_frequency
        self.frequency_list: Frequencies = frequencies
        self.data: AnalogData = AnalogData()


class ButtonProcessor:
    def __init__(self):
        self.buttons: List[ButtonProcessData] = []
        self.db: Database = Database()
        self._load_settings()

    def _load_settings(self):
        path_settings = get_project_root() / 'data/settings.json'
        with open(path_settings.resolve()) as f:
            settings = json.load(f)

        for name, button_settings in settings["buttons"].items():
            if button_settings["active"]:
                button = ButtonProcessData(name,
                                           button_settings["pin"],
                                           button_settings["apply_state"],
                                           Frequencies(settings["buttons"][name]["frequency"]["musicList"]))
                self.buttons.append(button)
                self.db.replace_button_data(name, button)

    def process(self, new_buttons_data: ButtonsData):
        # TODO: change from list to dict
        for state_new in new_buttons_data.get_data():
            for index, button_old in enumerate(self.buttons):
                if button_old.pin == state_new.pin:
                    if self._check_button_change(state_new, button_old.state):
                        self.buttons[index].process_data(new_buttons_data, self.buttons)
                        self.buttons[index].state = state_new

    @staticmethod
    def _check_button_change(state_new: ButtonState, state_old: ButtonState):
        if state_old == state_new:
            return False
        else:
            return True


class Equalizer:
    def __init__(self, reduction_60_hz: int = 0, reduction_170_hz: int = 0, reduction_310_hz: int = 0,
                 reduction_1_khz: int = 0, reduction_3_khz: int = 0, reduction_6_khz: int = 0,
                 reduction_12_hkz: int = 0):
        self.reduction_60_hz: int = reduction_60_hz
        self.reduction_170_hz: int = reduction_170_hz
        self.reduction_310_hz: int = reduction_310_hz
        self.reduction_1_khz: int = reduction_1_khz
        self.reduction_3_khz: int = reduction_3_khz
        self.reduction_6_khz: int = reduction_6_khz
        self.reduction_12_hkz: int = reduction_12_hkz

        self._iterator: int = 0

    def __iter__(self):
        return self

    def __next__(self):  # Python 2: def next(self)
        if self._iterator == 0:
            self._iterator += 1
            return self.reduction_60_hz
        if self._iterator == 1:
            self._iterator += 1
            return self.reduction_170_hz
        if self._iterator == 2:
            self._iterator += 1
            return self.reduction_310_hz
        if self._iterator == 3:
            self._iterator += 1
            return self.reduction_1_khz
        if self._iterator == 4:
            self._iterator += 1
            return self.reduction_3_khz
        if self._iterator == 5:
            self._iterator += 1
            return self.reduction_6_khz
        if self._iterator == 6:
            self._iterator += 1
            return self.reduction_12_hkz
        if self._iterator == 7:
            raise StopIteration

    def to_list(self) -> list:
        return [self.reduction_60_hz, self.reduction_170_hz, self.reduction_310_hz, self.reduction_1_khz,
                self.reduction_3_khz, self.reduction_6_khz, self.reduction_12_hkz]

    def from_list(self, data: list):
        self.reduction_60_hz: int = data[0]
        self.reduction_170_hz: int = data[1]
        self.reduction_310_hz: int = data[2]
        self.reduction_1_khz: int = data[3]
        self.reduction_3_khz: int = data[4]
        self.reduction_6_khz: int = data[5]
        self.reduction_12_hkz: int = data[6]


class AnalogItem:
    def __init__(self, name: str, pin: int, min_: int = 0, max_: int = 0, is_volume: bool = False,
                 is_frequency: bool = False, is_equalizer: bool = False):
        self.pin: int = pin
        self.name: str = name
        self.min: int = min_
        self.max: int = max_
        self.is_volume: bool = is_volume
        self.is_frequency: bool = is_frequency
        self.is_equalizer: bool = is_equalizer
        self.equalizer: Equalizer = Equalizer()
        self.value: int = 0
        self.frequency_list: Frequencies = Frequencies()
        self.buttons: List[str] = []


class AnalogProcessor:
    def __init__(self, publish_function):
        self.publish_function = publish_function

        self.db: Database = Database()

        self.analog_items: List[AnalogItem] = []

        self.settings = {}
        self.load_settings()

    def load_settings(self):
        with open(get_project_root() / 'data/settings.json') as f:
            self.settings = json.load(f)
        # TODO: make class out of this
        for name, item in self.settings["analog"]["sensors"].items():
            if item["on"]:
                analog_item = AnalogItem(
                    name=name,
                    pin=item["pin"],
                    is_frequency=item["is_frequency"],
                    is_volume=item["is_volume"],
                    is_equalizer=item["is_equalizer"]
                )
                if item["is_equalizer"]:
                    equalizer = item["equalizer"]
                    analog_item.equalizer.from_list(
                        [
                            equalizer["60Hz"],
                            equalizer["170Hz"],
                            equalizer["310Hz"],
                            equalizer["600Hz"],
                            equalizer["1kHz"],
                            equalizer["3kHz"],
                            equalizer["6kHz"],
                            equalizer["12kHz"]
                        ]
                    )
                self.analog_items.append(analog_item)
        for button_name, button_item in self.settings["buttons"].items():
            for index, analog_item in enumerate(self.analog_items):
                if button_item["frequency"]["pos"] == analog_item.name:
                    self.analog_items[index].frequency_list = Frequencies(button_item["frequency"]["musicList"])
                    self.analog_items[index].buttons.append(button_name)

    def process(self, data: AnalogData, active_actions: Actions):
        # TODO: multiple analog values must be possible
        for analog in data.get_data_sensor():
            for index, item in enumerate(self.analog_items):
                if item.pin == analog.pin:
                    if item.is_frequency:
                        value = self.set_frequency(item, analog.value, active_actions)
                        self.analog_items[index].value = value
                        break
                    elif item.is_volume:
                        value = self.set_volume(item, analog.value)
                        self.analog_items[index].value = value
                        break
                    elif item.is_equalizer:
                        value = self.set_equalizer(item, analog.value)
                        self.analog_items[index].value = value
                        break
                    else:
                        value = self.set_analog_sensor(item, analog.value)
                        self.analog_items[index].value = value
                        break

    def set_frequency(self, frequency_item: AnalogItem, current_frequency_value: int,
                      active_actions: Actions) -> int:
        if current_frequency_value == frequency_item.value:
            return current_frequency_value
        frequency_item.value = current_frequency_value
        self.set_stream(frequency_item, active_actions)
        self.db.replace_frequency(frequency_item.name, current_frequency_value)
        self.publish_function(f'{frequency_item.name}:{current_frequency_value}')
        return current_frequency_value

    def set_stream(self, frequency: AnalogItem, active_actions: Actions):
        if active_actions.is_empty():
            return None
        play_music_action = active_actions.get_play_music()
        if not play_music_action:
            return None
        if play_music_action.frequency_pin_name != frequency.name:
            return None
        button: ButtonProcessData = self.db.get_button_data(play_music_action.button_name)
        if not button:
            return None
        current_stream: str = self.db.get_stream()
        new_stream = button.get_frequency_stream(frequency.value)
        if new_stream != current_stream:
            self.db.replace_stream(new_stream)
            self.publish_function(f"stream:{new_stream}")

    @staticmethod
    def _map(max_: int, min_: int, value):
        return int(-(value - min_) / (min_ - max_) * 100)

    def set_volume(self, volume: AnalogItem, value: int) -> int:
        # volume = int(-(value - volume.min) / (volume.min - volume.max) * 100)
        value_new = self._map(volume.max, volume.min, value)
        if value_new < 0:
            value_new = 0
        elif value_new > 100:
            value_new = 100
        if volume.value == value_new:
            return value_new
        # print(f"Volume: {volume}")
        self.db.replace_volume(value_new)
        self.publish_function(f"volume:{value_new}")
        return value_new

    def set_analog_sensor(self, analog_item: AnalogItem, value: int) -> int:
        value_calc = int(-(value - analog_item.min) / (analog_item.min - analog_item.max) * 40) - 20
        if value_calc < 0:
            value_calc = 0
        elif value_calc > 100:
            value_calc = 100
        if value_calc == analog_item.value:
            return value_calc
        self.db.replace_bass(value_calc)
        self.publish_function(f"{analog_item.name}:{value_calc}")
        return value_calc

    def set_equalizer(self, frequency_item: AnalogItem, current_equalizer_value: int,
                      active_actions: Actions) -> int:
        if current_equalizer_value == frequency_item.value:
            return current_equalizer_value
        self.db.replace_equalizer_value(frequency_item.name, current_equalizer_value)
        msg = {"value": current_equalizer_value, "data": frequency_item.equalizer.to_list()}
        self.publish_function(f'equalizer:{str(msg)}')
        return current_equalizer_value
