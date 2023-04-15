import paho.mqtt.publish as publish
import time

MQTT_SERVER = "192.168.0.47"
MQTT_PATH = "test_channel"

while True:
    publish.single(MQTT_PATH, "Hello World!", hostname=MQTT_SERVER)  # send data continuously every 3 seconds
    print("send")
    time.sleep(3)
