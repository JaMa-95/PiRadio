import time

# Import the ADS1115 module.
# Create an ADS1115 ADC (16-bit) instance.
from ADS1x15 import ADS1115
adc = ADS1115()

# Import the ADS1015 module.
# Create an ADS1015 ADC (12-bit) instance.
#from ADS1x15 import ADS1015
#adc = ADS1015()

# Note you can change the I2C address from its default (0x48)
# bus by passing in these optional parameters:
#adc = ADS1115(address=0x49, busnum=1)

# Choose a gain of 1 for reading voltages from 0 to 4.09V.
GAIN = 1

print('+---------+---------+---------+---------+')
print('|    0    |    1    |    2    |    3    |')
print('+---------+---------+---------+---------+')

# Main loop.
while True:
    # Read all the ADC channel values in a list.
    value = adc.read_adc(0, gain=GAIN, data_rate=128)

    # Print the ADC values.
    print(f"value: {value}")

    # Pause for half a second.
    time.sleep(0.5)