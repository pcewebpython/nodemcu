import gc
import webrepl
webrepl.start()
gc.collect()

import network
import time
import machine

led_power = machine.Pin(2, machine.Pin.OUT)
led_power.value(0)

sta_if = network.WLAN(network.STA_IF); sta_if.active(True)

try:
    with open("passwords.txt") as f:
        connections = f.readlines()
except OSError:
    print("No passwords.txt file!")
    connections = []


for connection in connections:
    station, password = connection.split()

    print("Connecting to {}.".format(station))

    sta_if.connect(station, password)

    for i in range(30):
        print(".")

        if sta_if.isconnected():
            break

        time.sleep(1)

    if sta_if.isconnected():
        break
    else:
        print("Connection could not be made.\n")

if sta_if.isconnected():
    print("Connected as: {}".format(sta_if.ifconfig()[0]))

    led_wifi = machine.Pin(16, machine.Pin.OUT)

    for i in range(3):
        time.sleep(.5)
        led_wifi.value(1)
        time.sleep(.5)
        led_wifi.value(0)


