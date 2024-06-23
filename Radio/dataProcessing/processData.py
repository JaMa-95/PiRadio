from collections import deque
import time
from typing import List
from Radio.dataProcessing.states import ButtonClickStates
from Radio.dataProcessing.radioFrequency import Frequencies
from Radio.util.sensorMsg import AnalogData, ButtonState


class ButtonProcessData:
    def __init__(self, name: str, pin: int):
        self.name = name
        self.pin = pin
        self.state: ButtonState = ButtonState(pin=self.pin, state=False, states=deque([0]*ButtonState.max_values))
        self.short_threshold: int = 1
        self.long_threshold: int = 10
        self.radio_actions: list = []

    def add_radio_action(self, action):
        self.radio_actions.append(action)

    def get_radio_actions_to_activate(self) -> list:
        radio_actions = []
        states = self.get_click_states()
        for state in states:
            for action in self.radio_actions:
                if action.check_state(state):
                    radio_actions.append(action)
        return radio_actions

    def get_click_states(self) -> List[ButtonClickStates]:
        states = []
        if self.is_long_click():
            states.append(ButtonClickStates.BUTTON_STATE_LONG_CLICK)
        elif self.is_short_click():
            states.append(ButtonClickStates.BUTTON_STATE_SHORT_CLICK)
        if self.is_to_on():
            states.append(ButtonClickStates.BUTTON_STATE_ON)
        elif self.is_to_off():
            states.append(ButtonClickStates.BUTTON_STATE_OFF)
        if self.is_double_click():
            states.append(ButtonClickStates.BUTTON_STATE_DOUBLE_CLICK)
        return states

    def _is_click(self, threshold: int):
        # TODO: measure is click with time
        counter = 0
        for value in self.state.states:
            if value is True or value == 1:
                counter += 1
                if counter > threshold:
                    return True
            else:
                return False
        return False

    def is_to_on(self) -> bool:
        if self.state.states[0] and not self.state.states[1]:
            return True
        return False

    def is_to_off(self) -> bool:
        if not self.state.states[0] and self.state.states[1]:
            return True
        return False

    def is_short_click(self):
        counter = 0
        for index, value in enumerate(self.state.states):
            if index == 0 and (value is False or value == 0):
                pass
            elif (value is True or value == 1) and index > 0:
                counter += 1
            else:
                if counter > self.short_threshold and counter < self.long_threshold:
                    print("SHORT CLICK")
                    return True
                return False

    def is_long_click(self):
        counter = 0
        for index, value in enumerate(self.state.states):
            if index == 0 and (value is False or value == 0):
                pass
            elif value is True or value == 1:
                counter += 1
            else:
                if counter > self.long_threshold:
                    print("LONG CLICK")
                    return True
                return False

    def is_double_click(self):
        # TODO
        return False
        raise NotImplemented


class AnalogProcessData:
    def __init__(self, pin: int, name: str, is_frequency: bool, frequencies: Frequencies):
        self.name: str = name
        self.pin: int = pin
        self.is_frequency: bool = is_frequency
        self.frequency_list: Frequencies = frequencies
        self.data: AnalogData = AnalogData()
