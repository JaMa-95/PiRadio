from tapo_plug import tapoPlugApi


class TapoPlug:
    def __init__(self):
        self.device = {
            "tapoIp": "192.168.0.165",
            "tapoEmail": "jakob.mattes1995@web.de",
            "tapoPassword": "Uo5e6sk$sp"
        }

    def turn_off(self):
        response = tapoPlugApi.plugOff(self.device)

    def turn_on(self):
        response = tapoPlugApi.plugOn(self.device)