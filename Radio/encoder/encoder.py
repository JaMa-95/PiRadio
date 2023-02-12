import Encoder
import time

enc = Encoder.Encoder(16, 20)
while True:
        value = enc.read()
        print(value)
        time.sleep(0.01)

