import json
from typing import List

from Radio.collector.gpio.audioSourceSwitcher import AudioSourceSwitcher
from Radio.dataProcessing.processData import ButtonProcessData
from Radio.dataProcessing.radioFrequency import RadioFrequency, Frequencies
from Radio.db.db import Database
from Radio.util.dataTransmitter import Publisher
from Radio.util.sensorMsg import SensorMsg, ButtonState
from Radio.util.radioExceptions import PlayMusicActionError
from Radio.util.util import Singleton, get_project_root
from Radio.dataProcessing.states import ButtonClickStates, RadioActionTypes


class RadioAction:
    def __init__(self, apply_states: List[ButtonClickStates] = None, one_time_action: bool = False):
        if not apply_states:
            apply_states = []
        self.apply_states: List[ButtonClickStates] = apply_states
        self.one_time_action: bool = one_time_action

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def check_and_execute(self, button_click_state: ButtonClickStates, sensor_msg_new: SensorMsg,
                          sensor_msg_old: SensorMsg):
        if self.check_state(button_click_state):
            self.execute(sensor_msg_new, sensor_msg_old)

    def try_execute(self):
        pass

    # apply action to sensor msg
    def execute(self, sensor_msg_new: SensorMsg, sensor_msg_old: SensorMsg) -> SensorMsg:
        raise NotImplemented("This class is only used as a interface. Please, use one of the child classes")

    def execute_exit(self):
        pass

    def check_state(self, button_state: ButtonClickStates):
        print("Check state: ", button_state.value, " in ", self.apply_states)
        if button_state.value in self.apply_states:
            return True
        return False


class RadioActionFactory:
    @staticmethod
    def create(action_type: int, apply_states: List[ButtonState], button_name: str = "", frequency_pin_name: str = "") -> RadioAction:
        if action_type == RadioActionTypes.TURN_OFF_RASPBERRY.value:
            return TurnOffRaspberry(apply_states)
        elif action_type == RadioActionTypes.STOP_MUSIC.value:
            print("STOP MUSIC FOR: ", button_name)
            return TurnOffMusic(apply_states, button_name, frequency_pin_name)
        elif action_type == RadioActionTypes.PLAY_MUSIC.value:
            print("PLAY MUSIC FOR: ", button_name)
            return PlayMusic(apply_states, button_name, frequency_pin_name)
        elif action_type == RadioActionTypes.HOLD_FREQUENCY.value:
            return HoldFrequencyX(holding_pin_name=button_name, apply_states=apply_states)
        elif action_type == RadioActionTypes.ROTATE_AUDIO_SOURCE.value:
            return RotateAudioSource(apply_states)
        elif action_type == RadioActionTypes.SET_AUDIO_SOURCE.value:
            return SwitchAudioSource(apply_states, switch_to=frequency_pin_name)
        else:
            # not implemented
            return RadioAction(apply_states)


class OffRestriction(RadioAction):
    def __init__(self, exception_pin: list, apply_states: List[ButtonClickStates]):
        super().__init__(apply_states)
        self.exception_pin: int = exception_pin

    def execute(self, sensor_msg_new: SensorMsg, sensor_msg_old: SensorMsg) -> SensorMsg:
        updated_buttons = []
        for button in sensor_msg_old.buttons_data.get_data():
            if button.pin not in self.exception_pin:
                updated_buttons.append(
                    ButtonState(button.pin, False, [False])
                )
            else:
                updated_buttons.append(button)
        sensor_msg_new.buttons_data.set_data(updated_buttons)
        return sensor_msg_new


class HoldFrequencyX(RadioAction):
    def __init__(self, holding_pin_name: str, apply_states: [ButtonClickStates]):
        super().__init__(apply_states)
        self.holding_pin_name: str = holding_pin_name
        self.holding_frequency_pin: List[int] = self.get_holding_pins(holding_pin_name)

    @staticmethod
    def get_holding_pins(holding_pin_name: str) -> List[int]:
        path_settings = get_project_root() / 'data/settings.json'
        with open(path_settings.resolve()) as f:
            settings = json.load(f)
        for action_settings in settings["buttons"][holding_pin_name]["action"]:
            if "holding_pins" in action_settings:
                return action_settings["holding_pins"]

    def execute(self, sensor_msg_new: SensorMsg, sensor_msg_old: SensorMsg) -> SensorMsg:
        for index, frequency_data in enumerate(sensor_msg_new.analog_data.sensor_data):
            for index_old, frequency_data_old in enumerate(sensor_msg_old.analog_data.sensor_data):
                for holding_pin in self.holding_frequency_pin:
                    if frequency_data.pin == holding_pin and frequency_data_old.pin == holding_pin:
                        sensor_msg_new.analog_data.sensor_data[index].value = (
                            sensor_msg_old.analog_data.sensor_data[index_old].value)
                        return sensor_msg_new


class PlayMusic(RadioAction):
    def __init__(self, apply_states: [ButtonClickStates], button_name, frequency_pin_name):
        super().__init__(apply_states=apply_states)
        self.button_name: str = button_name
        self.frequency_pin_name: str = frequency_pin_name
        self.db: Database = Database()
        self.publisher: Publisher = Publisher()
        self.frequency_list: Frequencies = self.get_frequency_list()

    def get_frequency_list(self) -> Frequencies:
        with open(get_project_root() / 'data/settings.json') as f:
            settings = json.load(f)
        return Frequencies(settings["buttons"][self.button_name]["frequency"]["musicList"])

    def execute(self, sensor_msg_new: SensorMsg, sensor_msg_old: SensorMsg) -> SensorMsg:
        self.play_music()

    def try_execute(self):
        self.play_music()

    def play_music(self):
        button: ButtonProcessData = self.db.get_button_data(self.button_name)
        if not button:
            return None
        radio_frequency: RadioFrequency = self.get_radio_frequency()
        if not radio_frequency:
            return None
        current_radio_frequency = self.db.get_radio_frequency()
        if (radio_frequency.radio_url == current_radio_frequency.radio_url and
                radio_frequency.radio_url_re == current_radio_frequency.radio_url_re and
                radio_frequency.name == current_radio_frequency.name) or not radio_frequency:
            return None
        self.db.replace_radio_frequency(radio_frequency)
        if radio_frequency.re_active:
            url = radio_frequency.radio_url_re
        else:
            url = radio_frequency.radio_url
        self.publisher.publish(f"stream:{url}")
        self.db.replace_active_radio_url(url)

    def get_radio_frequency(self) -> None | RadioFrequency:
        sensor_value = self.db.get_frequency_value(self.frequency_pin_name)
        over_min_max_frequency = None
        # print("------------------------------------------------------")
        for index, radio_frequency in enumerate(self.frequency_list.frequencies):
           # print(radio_frequency.minimum, radio_frequency.maximum, sensor_value)
            try:
                if radio_frequency.minimum <= sensor_value < radio_frequency.maximum:
                    return radio_frequency
                elif index == 0 and sensor_value < radio_frequency.minimum:
                    over_min_max_frequency = radio_frequency
                elif index == len(self.frequency_list.frequencies) and sensor_value > radio_frequency.maximum:
                    over_min_max_frequency = radio_frequency
            except TypeError as error:
                print("Error: ", error)
                return None
        return over_min_max_frequency

    def execute_exit(self):
        print("Stop music")
        self.publisher.publish("stop")
        self.db.replace_active_radio_url("")


class TurnOffMusic(RadioAction):
    def __init__(self, apply_states: List[ButtonClickStates], button_name, frequency_pin_name):
        super().__init__(apply_states=apply_states)
        self.button_name: str = button_name
        self.frequency_pin_name: str = frequency_pin_name
        self.db: Database = Database()
        self.publisher: Publisher = Publisher()

    def execute(self, sensor_msg_new: SensorMsg, sensor_msg_old: SensorMsg) -> SensorMsg:
        self.stop_music()

    def try_execute(self) -> bool:
        self.stop_music()
        return True

    def stop_music(self):
        self.db.replace_radio_frequency(RadioFrequency())
        self.publisher.publish(f"stop")
        self.db.replace_active_radio_url("")


class TurnOffRaspberry(RadioAction):
    def execute(self, sensor_msg_new: SensorMsg, sensor_msg_old: SensorMsg) -> SensorMsg:
        raise NotImplemented("Turn off raspi")


class AddRestriction(RadioAction):
    def execute(self, sensor_msg_new: SensorMsg, sensor_msg_old: SensorMsg) -> SensorMsg:
        raise NotImplemented("Add restriction")


class SwitchAudioSource(RadioAction):
    def __init__(self, apply_states: List[ButtonClickStates], switch_to: str):
        super().__init__(apply_states=apply_states, one_time_action=True)
        self.audio_source_switcher: AudioSourceSwitcher = AudioSourceSwitcher()
        self.swtich_to: str = switch_to
        self.value_a: bool = False
        self.value_b: bool = False
        self.load_from_settings()

    def load_from_settings(self):
        path_settings = get_project_root() / 'data/settings.json'
        with open(path_settings.resolve()) as f:
            settings = json.load(f)
        for switch_device in settings["audio"]["switcher"]["devices"]:
            if switch_device["device"] == self.swtich_to:
                self.value_a = switch_device["A"]
                self.value_b = switch_device["B"]

    def execute(self, sensor_msg_new: SensorMsg, sensor_msg_old: SensorMsg) -> SensorMsg:
        self.audio_source_switcher.switch(self.value_a, self.value_b)
        return sensor_msg_new
    
class RotateAudioSource(RadioAction):
    def __init__(self, apply_states: List[ButtonClickStates]):
        super().__init__(apply_states=apply_states, one_time_action=True)
        self.audio_source_switcher: AudioSourceSwitcher = AudioSourceSwitcher()

    def execute(self, sensor_msg_new: SensorMsg, sensor_msg_old: SensorMsg) -> SensorMsg:
        self.audio_source_switcher.rotate_source()
        return sensor_msg_new
    
    def try_execute(self) -> SensorMsg:
        self.execute(None, None)
        

class Actions(Singleton):
    def __init__(self):
        self._actions: List[RadioAction] = []

    def get_play_music(self) -> None | RadioAction:
        # TODO: error when multiple or return multiple
        action_return = None
        for action in self._actions:
            if isinstance(action, PlayMusic):
                if action_return:
                    None
                    # raise PlayMusicActionError("Multiple play music actions at the same time not supported")
                action_return = action
        return action_return

    def is_empty(self):
        if not self._actions:
            return True
        return False

    def process(self, sensor_msg_current: SensorMsg, sensor_msg_old: SensorMsg):
        for action in self._actions:
            sensor_msg_current_return = action.execute(sensor_msg_new=sensor_msg_current,
                                                       sensor_msg_old=sensor_msg_old)
            if sensor_msg_current_return:
                sensor_msg_current = sensor_msg_current_return
        return sensor_msg_current

    def add_action(self, action: RadioAction):
        self._actions.append(action)

    def remove_action(self, action_new: RadioAction):
        for index, action in enumerate(self._actions):
            if action == action_new:
                self._actions.pop(index)

    def remove_all_of_type(self, typ_: RadioAction):
        for index, action in enumerate(self._actions):
            if isinstance(action, typ_):
                self._actions.pop(index)

    def add_or_remove_action(self, action_new: RadioAction):
        print("Add or remove action: ", action_new.__class__)
        if len(self._actions) > 0:
            for index, action in enumerate(self._actions):
                if isinstance(action_new, TurnOffMusic):
                    self.remove_all_of_type(PlayMusic)
                    action_new.try_execute()
                    break
                elif action == action_new:
                    self._actions[index].execute_exit()
                    self._actions.pop(index)
                    break
                elif action.one_time_action:
                    action_new.try_execute()
                    break
                else:
                    action_new.try_execute()
                    self._actions.append(action_new)
                    break
        else:
            if isinstance(action_new, TurnOffMusic):
                self.remove_all_of_type(PlayMusic)
                action_new.try_execute()
            elif action_new.one_time_action:
                print("TRY EXECUTE")
                action_new.try_execute()
            else:
                action_new.try_execute()
                self._actions.append(action_new)

    def add_or_remove_actions(self, actions_new: List[RadioAction]):
        for action in actions_new:
            self.add_or_remove_action(action)
