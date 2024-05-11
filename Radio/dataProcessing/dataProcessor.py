import json
import time
from typing import List

from Radio.dataProcessing.RadioAction import RadioAction, ButtonClickStates, Actions, RadioActionFactory
from Radio.dataProcessing.equalizerData import Equalizer, EqualizerReductionData
from Radio.dataProcessing.processData import ButtonProcessData
from Radio.db.db import Database
from Radio.util.sensorMsg import SensorMsg, ButtonsData, AnalogData, ButtonState, SensorData, SensorDataOld
from Radio.util.dataTransmitter import DataTransmitter, Publisher
from Radio.util.util import get_project_root
from Radio.dataProcessing.radioFrequency import Frequencies, RadioFrequency


class DataProcessor:
    def __init__(self, publisher: Publisher):
        self.data_transmitter: DataTransmitter = DataTransmitter()
        self.publisher: Publisher = publisher

        self.button_processor: ButtonProcessor = ButtonProcessor()
        self.analog_processor: AnalogProcessor = AnalogProcessor(self.publisher.publish)

        self.sensor_msg_old: SensorMsg = SensorMsg()

        self.active_actions: Actions = Actions()

        self.cycle_time: float = 0.0

        self.pin_frequencies: int = 0
        self.pin_volume: int = 0
        self.pin_bass: int = 0
        self.pin_treble: int = 0

        self.settings: dict = {}
        self.load_settings()

        self.db: Database = Database()

    def load_settings(self):
        with open(get_project_root() / 'data/settings.json') as f:
            self.settings = json.load(f)

        self.cycle_time = self.settings["cycle_time"]

    def run(self):
        while True:
            # TODO: wait instead of endless loop
            if self.data_transmitter.has_data():
                sensor_msg_current = self.data_transmitter.receive()
                sensor_msg_current = self.active_actions.process(sensor_msg_current=sensor_msg_current,
                                                                 sensor_msg_old=self.sensor_msg_old)
                self.process_analogs(sensor_msg_current.analog_data)
                self.process_buttons(sensor_msg_current)
                self.sensor_msg_old = sensor_msg_current
            else:
                time.sleep(self.cycle_time)

    # mostly for testing purpose
    def add_remove_actions(self, action: RadioAction):
        self.active_actions.add_or_remove_action(action)

    def process_buttons(self, sensor_msg_current: SensorMsg):
        self.active_actions.add_or_remove_actions(self.button_processor.process(sensor_msg_current))

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


class ButtonProcessor:
    def __init__(self):
        self.buttons: List[ButtonProcessData] = []
        self.db: Database = Database()
        self.action_factory: RadioActionFactory = RadioActionFactory()
        self._load_settings()

    def _load_settings(self):
        path_settings = get_project_root() / 'data/settings.json'
        with open(path_settings.resolve()) as f:
            settings = json.load(f)

        for name, button_settings in settings["buttons"].items():
            if button_settings["active"]:
                # TODO: append happening
                button = ButtonProcessData(name,
                                           button_settings["pin"],
                                           Frequencies(settings["buttons"][name]["frequency"]["musicList"]))
                radio_action = self.action_factory.create(
                    action_type=button_settings["action"]["type"],
                    apply_states=button_settings["action"]["apply_state"],
                    button_name=name,
                    button_pin=button_settings["pin"],
                    frequency_pin_name=button_settings["frequency"]["pos"]
                )
                button.set_radio_action(radio_action)
                self.buttons.append(button)
                self.db.replace_button_data(name, button)

    def process(self, sensor_msg_current: SensorMsg):
        # TODO: change from list to dict
        new_actions = []
        for state_new in sensor_msg_current.buttons_data.get_data():
            for index, button_old in enumerate(self.buttons):
                if button_old.pin == state_new.pin:
                    if self._check_button_change(state_new, button_old.state):
                        new_actions.append(self.buttons[index].radio_action)
                        self.buttons[index].state = state_new
        return new_actions

    @staticmethod
    def _check_button_change(state_new: ButtonState, state_old: ButtonState):
        if state_old == state_new:
            return False
        else:
            return True


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

        # TODO: nicer solution
        self.is_first_run: bool = True

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
                    equalizer = item["equalizer_reduction"]
                    analog_item.equalizer.reduction.from_list(
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
        # TODO: smarter solution
        for analog in data.get_data_sensor():
            for index, item in enumerate(self.analog_items):
                if item.pin == analog.pin:
                    if self.is_first_run:
                        item.max = analog.max
                        item.min = analog.min
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
                        raise NotImplemented
        self.is_first_run = False

    def set_frequency(self, frequency_item: AnalogItem, current_frequency_value: int,
                      active_actions: Actions) -> int:
        if current_frequency_value == frequency_item.value:
            return current_frequency_value
        frequency_item.value = current_frequency_value
        self.set_stream(frequency_item, active_actions)
        self.db.replace_frequency(frequency_item.name, current_frequency_value)
        self.publish_function(f'{frequency_item.name}:{current_frequency_value}')
        return current_frequency_value

    @staticmethod
    def set_stream(frequency: AnalogItem, active_actions: Actions):
        if active_actions.is_empty():
            return None
        play_music_action = active_actions.get_play_music()
        if not play_music_action:
            return None
        if play_music_action.frequency_pin_name != frequency.name:
            return None
        play_music_action.try_execute()

    @staticmethod
    def _map(max_: int, min_: int, value):
        if min_ - max_ == 0:
            raise ValueError("Min and max cant be 0")
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

    def set_equalizer(self, frequency_item: AnalogItem, current_equalizer_value: int) -> int:
        if current_equalizer_value == frequency_item.value:
            return current_equalizer_value
        frequency_item.equalizer.calc_equalizer_with_reductions(current_equalizer_value)
        self.db.replace_equalizer(frequency_item.equalizer)
        self.publish_function(f'equalizer:{str(frequency_item.equalizer.to_list())}')
        return current_equalizer_value
