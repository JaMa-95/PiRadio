import random
import vlc
from paho.mqtt import client as mqtt_client


class MqttClient:
    def __init__(self):
        self.broker = "192.168.0.47"
        self.port = 1883
        self.topic = "piradio/start"
        # generate client ID with pub prefix randomly
        self.client_id = f'python-mqtt-{random.randint(0, 100)}'
        self.username = 'picentral'
        self.password = 'picentral'
        self.client = None

        self.topic_start = "piradio/start"
        self.topic_stream = "piradio/stream"
        self.topic_volume = "piradio/volume"

        self.instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
        self.player = self.instance.media_player_new()
        self.volume = 50
        self.url = None
        self.start = "0"

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    def connect_mqtt(self) -> mqtt_client:
        self.client = mqtt_client.Client(self.client_id)
        self.client.username_pw_set(self.username, self.password)
        self.client.on_connect = self.on_connect
        self.client.connect(self.broker, self.port)

    def subscribe(self: mqtt_client):
        self.client.subscribe(self.topic_start)
        self.client.subscribe(self.topic_volume)
        self.client.subscribe(self.topic_stream)
        self.client.on_message = self.on_message

    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode()
        print(f"Received `{payload}` from `{msg.topic}` topic")
        topic = msg.topic
        a = msg.payload.decode()
        if topic == self.topic_start:
            self.set_start(start=msg.payload.decode())
        elif topic == self.topic_volume:
            self.set_volume(volume=int(msg.payload.decode()))
        elif topic == self.topic_stream:
            self.set_stream(url=msg.payload.decode())

    def set_start(self, start):
        print(f"Start/Stop: {start}")
        self.start = start
        if self.start == "0":
            self.stop()
        else:
            if self.url is not None:
                self.play()

    def run(self):
        self.connect_mqtt()
        self.subscribe()
        self.client.loop_forever()

    def set_stream(self, url):
        print(f"Set stream: {url}")
        self.url = url
        self.stop()
        media = self.instance.media_new(self.url)
        media.get_mrl()
        self.player.set_media(media)
        if self.start == "1":
            self.player.play()

    def play(self):
        self.player.play()

    def stop(self):
        self.player.stop()

    def set_volume(self, volume):
        volume = int(volume * 3)
        if self.player:
            self.player.audio_set_volume(volume)
        self.volume = volume


if __name__ == '__main__':
    MqttClient().run()
