import Encoder
import time

enc = Encoder.Encoder(6, 13)
while True:
        value = enc.read()
        print(value)
        time.sleep(0.01)

