import datetime


class Button:
    def __init__(self, click_threshold: int, long_click_threshold):
        self.value: int = None
        self.value_old = []
        self.threshold: int = click_threshold
        self.long_threshold: int = long_click_threshold
        self.indexer = 0

        self.last_click: list = [None, None]
        self.last_click_index: int = 0

        self.is_clicked: bool = False

    def is_click(self):
        if self.value < self.threshold:
            return True
        return False

    def double_click(self):
        time_delta_a = self.last_click[0] - self.last_click[1]
        time_delta_b = self.last_click[1] - self.last_click[0]
        if time_delta_a.seconds < 4 or time_delta_b.seconds < 4:
            return True
        return False

    def reset_double_click(self):
        self.last_click[0] = None
        self.last_click[1] = None

    def long_click(self):
        if self.indexer > self.long_threshold:
            return True
        return False

    def get_value(self):
        return self.value

    def set_value(self, value: int):
        self.value = value
        if value < 30:
            self.is_clicked = True
            self.indexer += 1
        else:
            self.is_clicked = False
            self.indexer = 0

    def get_last_clicked_index(self):
        self.last_click_index = (self.last_click_index + 1) % 2
        return self.last_click_index

    def set_is_clicked(self, value: bool):
        if self.is_clicked and not value:
            self.last_click[self.get_last_clicked_index()] = datetime.datetime.now()
        self.is_clicked = value
