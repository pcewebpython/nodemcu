# A led blinking every half second for five times.
import time

from machine import Pin


# create an output pin on pin #2
# because for ESP-12 board the led light using GPIO2 which is pin2.
# the led operate in "inverted" mode, which means the pin value is '1' will set
# the led off, and pin value "0" will set the led on.
led = Pin(2, Pin.OUT)
# set the value high to turn the led off.
led.value(1)
time.sleep(1)
for i in range(5):
    time.sleep(.5)
    led.value(0)
    time.sleep(.5)
    led.value(1)
