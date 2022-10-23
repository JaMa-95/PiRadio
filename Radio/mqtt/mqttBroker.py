import random
import time

from paho.mqtt import client as mqtt_client


class MqttBroker:
    def __init__(self):
        self.broker = "localhost"
        self.port = 1883
        self.topic_start = "piradio/start"
        self.topic_stream = "piradio/stream"
        self.topic_volume = "piradio/volume"
        # generate client ID with pub prefix randomly
        self.client_id = f'python-mqtt-{random.randint(0, 1000)}'
        self.username = 'piradio'
        self.password = 'piradio'
        self.client = None

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    def connect_mqtt(self):

        self.client = mqtt_client.Client(self.client_id)
        self.client.username_pw_set(self.username, self.password)
        self.client.on_connect = self.on_connect
        self.client.connect(self.broker, self.port)

    def publish_start_stop(self, start: False):
        print("publish start/stop")
        result = self.client.publish(self.topic_start, start)
        status = result[0]
        if status != 0:
            print(f"Failed to send message to topic {self.topic_start}")

    def publish_volume(self, volume):
        print("publish volume")
        result = self.client.publish(self.topic_volume, volume)
        status = result[0]
        if status != 0:
            print(f"Failed to send message to topic {self.topic_volume}")

    def publish_stream(self, stream: None):
        print("publish stream")
        result = self.client.publish(self.topic_stream, stream)
        status = result[0]
        if status != 0:
            print(f"Failed to send message to topic {self.topic_stream}")


    def publish(self):
        msg_count = 0
        while True:
            time.sleep(1)
            msg = f"{msg_count}"
            result = self.client.publish(self.topic_start, msg)
            # result: [0, 1]
            status = result[0]
            if status == 0:
                print(f"Send `{msg}` to topic `{self.topic_start}`")
            else:
                print(f"Failed to send message to topic {self.topic_start}")
            msg_count += 1

    def run(self):
        self.connect_mqtt()
        self.client.loop_start()
        self.publish()


if __name__ == '__main__':
    broker = MqttBroker()
    broker.connect_mqtt()
    broker.client.loop_start()
    broker.publish_stream("123")
    broker.publish_volume(12)
    broker.publish_start_stop("0")