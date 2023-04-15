from tapo_plug import tapoPlugApi


class TapoPlug:
    def __init__(self):
        self.device = {
            "tapoIp": "--",
            "tapoEmail": "--",
            "tapoPassword": "--"
        }

    def turn_off(self):
        response = tapoPlugApi.plugOff(self.device)

    def turn_on(self):
        response = tapoPlugApi.plugOn(self.device)