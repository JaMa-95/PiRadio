from enum import Enum
from typing import List
from Radio.sensorMsg import SensorMsg, ButtonState
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

    def execute(self, button_click_state: ButtonClickStates, sensor_msg_current: SensorMsg,
                sensor_msg_old: SensorMsg):
        if self.apply(button_click_state):
            self._execute(sensor_msg_current, sensor_msg_old)

    def _execute(self, sensor_msg_current: SensorMsg, sensor_msg_old: SensorMsg) -> SensorMsg:
        raise NotImplemented

    def apply(self, button_state: ButtonClickStates):
        if button_state in self.apply_states:
            return True
        return False


class OffRestriction(RadioAction):
    def __init__(self, exception_pin: [], apply_states: [ButtonClickStates]):
        super().__init__(apply_states)
        self.exception_pin: int = exception_pin

    def _execute(self, sensor_msg_current: SensorMsg, sensor_msg_old: SensorMsg) -> SensorMsg:
        updated_buttons = []
        for button in sensor_msg_current.buttons_data.get_data():
            if button.pin not in self.exception_pin:
                updated_buttons.append(
                    ButtonState(button.pin, False, [False])
                )
            else:
                updated_buttons.append(button)
        sensor_msg_current.buttons_data.set_data(updated_buttons)
        return sensor_msg_current


class HoldFrequencyX(RadioAction):
    def __init__(self, holding_pin: int, apply_states: [ButtonClickStates]):
        super().__init__(apply_states)
        self.holding_pin: int = holding_pin

    def _execute(self, sensor_msg_current: SensorMsg, sensor_msg_old: SensorMsg) -> SensorMsg:
        sensor_msg_current.buttons_data.update_value(self.holding_pin,
                                                     sensor_msg_old.buttons_data.get_value(self.holding_pin))
        return sensor_msg_current


class PlayMusic(RadioAction):
    pass


class TurnOffMusic(RadioAction):
    pass


class TurnOffRaspberry(RadioAction):
    pass


class AddRestriction(RadioAction):
    pass


class Restrictions(Singleton):
    def __init__(self):
        self.restrictions: List[RadioAction] = []

    def add_restriction(self, restriction: RadioAction):
        self.restrictions.append(restriction)

    def remove_restriction(self, restriction_new: RadioAction):
        for index, restriction in enumerate(self.restrictions):
            if restriction == restriction_new:
                self.restrictions.pop(index)

    def add_or_remove_restriction(self, restriction_new: RadioAction):
        for index, restriction in enumerate(self.restrictions):
            if restriction == restriction_new:
                self.restrictions.pop(index)
        self.restrictions.append(restriction_new)


