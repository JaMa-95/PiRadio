import json
from enum import Enum
from typing import List

from Radio.dataProcessing.processData import ButtonProcessData
from Radio.dataProcessing.radioFrequency import RadioFrequency
from Radio.db.db import Database
from Radio.util.dataTransmitter import Publisher
from Radio.util.sensorMsg import SensorMsg, ButtonState
from Radio.util.radioExceptions import PlayMusicActionError
from Radio.util.util import Singleton, get_project_root
from Radio.dataProcessing.states import ButtonClickStates


class RadioAction:
    def __init__(self, apply_states: [ButtonClickStates] = None):
        if not apply_states:
            apply_states = []
        self.apply_states: [ButtonClickStates] = apply_states

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
        if button_state.value in self.apply_states:
            return True
        return False


class RadioActionFactory:
    @staticmethod
    def create(action_type: int, apply_states: [ButtonState], button_name: str = "", button_pin: int = 0,
               frequency_pin_name: str = "") \
            -> RadioAction:
        if action_type == 0:
            return TurnOffRaspberry(apply_states)
        elif action_type == 1:
            return TurnOffMusic(apply_states)
        elif action_type == 2:
            return PlayMusic(apply_states, button_name, frequency_pin_name)
        elif action_type == 3:
            return HoldFrequencyX(button_name, frequency_pin_name, apply_states)
        else:
            # not implemented
            return RadioAction(apply_states)


class OffRestriction(RadioAction):
    def __init__(self, exception_pin: [], apply_states: [ButtonClickStates]):
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
    def __init__(self, holding_pin_name: str, holding_frequency_pin_name: str, apply_states: [ButtonClickStates]):
        super().__init__(apply_states)
        self.holding_pin_name: str = holding_pin_name
        self.holding_frequency_pin: int = self.get_frequency_pin(holding_frequency_pin_name)

    @staticmethod
    def get_frequency_pin(frequency_name: str) -> int:
        with open(get_project_root() / 'data/settings.json') as f:
            settings = json.load(f)
        for name, item in settings["analog"]["sensors"].items():
            if name == frequency_name:
                return item["pin"]

    def execute(self, sensor_msg_new: SensorMsg, sensor_msg_old: SensorMsg) -> SensorMsg:
        for index, frequency_data in enumerate(sensor_msg_new.analog_data.sensor_data):
            for index_old, frequency_data_old in enumerate(sensor_msg_old.analog_data.sensor_data):
                if (frequency_data.pin == self.holding_frequency_pin and frequency_data_old.pin ==
                        self.holding_frequency_pin):
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

    def execute(self, sensor_msg_new: SensorMsg, sensor_msg_old: SensorMsg) -> SensorMsg:
        self.play_music()

    def try_execute(self):
        self.play_music()

    def play_music(self):
        button: ButtonProcessData = self.db.get_button_data(self.button_name)
        if not button:
            return None
        radio_frequency: RadioFrequency = self.db.get_radio_frequency()
        if radio_frequency.re_active:
            url = radio_frequency.radio_url_re
        else:
            url = radio_frequency.radio_url
        self.publisher.publish(f"stream:{url}")
        self.db.replace_active_radio_url(url)

    def execute_exit(self):
        self.publisher.publish("stream:")
        self.db.replace_active_radio_url("")


class TurnOffMusic(RadioAction):
    def execute(self, sensor_msg_new: SensorMsg, sensor_msg_old: SensorMsg) -> SensorMsg:
        raise NotImplemented("Turn off music")


class TurnOffRaspberry(RadioAction):
    def execute(self, sensor_msg_new: SensorMsg, sensor_msg_old: SensorMsg) -> SensorMsg:
        pass
        #raise NotImplemented("Turn off raspi")


class AddRestriction(RadioAction):
    def execute(self, sensor_msg_new: SensorMsg, sensor_msg_old: SensorMsg) -> SensorMsg:
        raise NotImplemented("Add restriction")


class Actions(Singleton):
    def __init__(self):
        self._actions: List[RadioAction] = []

    def get_play_music(self) -> None | RadioAction:
        # TODO: error when multiple or return multiple
        action_return = None
        for action in self._actions:
            if isinstance(action, PlayMusic):
                if action_return:
                    raise PlayMusicActionError("Multiple play music actions at the same time not supported")
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

    def add_or_remove_action(self, action_new: RadioAction):
        for index, action in enumerate(self._actions):
            if action == action_new:
                self._actions[index].execute_exit()
                self._actions.pop(index)
        action_new.try_execute()
        self._actions.append(action_new)

    def add_or_remove_actions(self, actions_new: List[RadioAction]):
        for action in actions_new:
            self.add_or_remove_action(action)
