import time

from machine import Pin


led = Pin(2, Pin.OUT)
for i in range(3):
    time.sleep(.5)
    led.value(1)
    time.sleep(.5)
    led.value(0)

