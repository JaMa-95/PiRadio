from enum import Enum
from typing import List
from Radio.util.sensorMsg import SensorMsg, ButtonState
from Radio.util.radioExceptions import PlayMusicActionError
from Radio.util.util import Singleton


class ButtonClickStates(Enum):
    BUTTON_STATE_OFF = 0
    BUTTON_STATE_ON = 1
    BUTTON_STATE_SHORT_CLICK = 2
    BUTTON_STATE_LONG_CLICK = 3
    BUTTON_STATE_DOUBLE_CLICK = 4


class RadioAction:
    def __init__(self, apply_states: [ButtonClickStates]):
        self.apply_states: [ButtonClickStates] = apply_states

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def check_and_execute(self, button_click_state: ButtonClickStates, sensor_msg_new: SensorMsg,
                          sensor_msg_old: SensorMsg):
        if self.check_state(button_click_state):
            self.execute(sensor_msg_new, sensor_msg_old)

    # apply action to sensor msg
    def execute(self, sensor_msg_new: SensorMsg, sensor_msg_old: SensorMsg) -> SensorMsg:
        raise NotImplemented("This class is only used as a interface. Please, use one of the child classes")

    def check_state(self, button_state: ButtonClickStates):
        if button_state in self.apply_states:
            return True
        return False


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
    def __init__(self, holding_pin: int, holding_frequency_pin: int, apply_states: [ButtonClickStates]):
        super().__init__(apply_states)
        self.holding_pin: int = holding_pin
        self.holding_frequency_pin: int = holding_frequency_pin

    def execute(self, sensor_msg_new: SensorMsg, sensor_msg_old: SensorMsg) -> SensorMsg:
        for index, frequency_data in enumerate(sensor_msg_new.analog_data.sensor_data):
            for index_old, frequency_data_old in enumerate(sensor_msg_old.analog_data.sensor_data):
                if (frequency_data.pin == self.holding_frequency_pin and frequency_data_old.pin ==
                        self.holding_frequency_pin):
                    sensor_msg_new.analog_data.sensor_data[index].value  = (
                        sensor_msg_old.analog_data.sensor_data[index_old].value)
                    return sensor_msg_new


class PlayMusic(RadioAction):
    def __init__(self, apply_states: [ButtonClickStates], button_name, frequency_pin_name):
        super().__init__(apply_states=apply_states)
        self.button_name: str = button_name
        self.frequency_pin_name: str = frequency_pin_name



class TurnOffMusic(RadioAction):
    pass


class TurnOffRaspberry(RadioAction):
    pass


class AddRestriction(RadioAction):
    pass


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
            sensor_msg_current = action.execute(sensor_msg_current=sensor_msg_current,
                                                     sensor_msg_old=sensor_msg_old)
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
                self._actions.pop(index)
        self._actions.append(action_new)


