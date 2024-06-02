from enum import Enum


class ButtonClickStates(Enum):
    BUTTON_STATE_OFF = 0
    BUTTON_STATE_ON = 1
    BUTTON_STATE_SHORT_CLICK = 2
    BUTTON_STATE_LONG_CLICK = 3
    BUTTON_STATE_DOUBLE_CLICK = 4
    BUTTON_STATE_TO_ON = 5
    BUTTON_STATE_TO_OFF = 6


class RadioActionTypes(Enum):
    TURN_OFF_RASPBERRY = 0
    STOP_MUSIC = 1
    PLAY_MUSIC = 2
    HOLD_FREQUENCY = 3