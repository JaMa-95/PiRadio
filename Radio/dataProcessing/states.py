from enum import Enum


class ButtonClickStates(Enum):
    BUTTON_STATE_OFF = 0
    BUTTON_STATE_ON = 1
    BUTTON_STATE_SHORT_CLICK = 2
    BUTTON_STATE_LONG_CLICK = 3
    BUTTON_STATE_DOUBLE_CLICK = 4