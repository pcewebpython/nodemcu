import gc
import webrepl
webrepl.start()
gc.collect()

import network
import time
import machine

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

    for i in range(15):
        print(".")

        if sta_if.isconnected():
            break

        time.sleep(1)

    if sta_if.isconnected():
        break
    else:
        print("Connection could not be made.\n")



builtin_led = machine.Pin(16, machine.Pin.OUT)

def blink(length):
    builtin_led.value(0)
    time.sleep(length)
    builtin_led.value(1)

if sta_if.isconnected():
    ip = sta_if.ifconfig()[0].split('.')[3]
    print("Connected as: {}".format(ip))


    for digit in ip:
        blink(.1)
        time.sleep(.1)
        blink(.1)
        time.sleep(2)

        for i in range(int(digit)):
            blink(.5)
            time.sleep(.5)

        time.sleep(2)
        
        
