try:
    import usocket as socket
except:
    import socket

response_404 = """HTTP/1.0 404 NOT FOUND

<h1>404 Not Found</h1>
"""

response_500 = """HTTP/1.0 500 INTERNAL SERVER ERROR

<h1>500 Internal Server Error</h1>
"""

response_template = """HTTP/1.0 200 OK

%s
"""

import machine
import ntptime, utime
from machine import RTC
from time import sleep

try:
    seconds = ntptime.time()
except:
    seconds = 0

rtc = RTC()
rtc.datetime(utime.localtime(seconds))

def time():
    body = """<html>
<body>
<h1>Time</h1>
<p>%s</p>
</body>
</html>
""" % str(rtc.datetime())
    return response_template % body

def dummy():
    body = "This is a dummy endpoint"
    return response_template % body
# ------------------------------------

on_off_pin = machine.Pin(16, machine.Pin.OUT)

def light_on():
     on_off_pin.value(0)
     body = "You turned a light on!"
     return response_template % body

def light_off():
     on_off_pin.value(1)
     body = "You turned a light off!"
     return response_template % body
# ------------------------------------

switch_pin = machine.Pin(5, machine.Pin.IN)
def switch():
     body = "{state: " + str(switch_pin.value()) + "}"
     return response_template % body

# Port 10 is always in high impedance mode on my microcontroller,
# which prevents wifi connection to router. Instead, I used port 5 (GPI05). 
# ------------------------------------

adc_pin = machine.ADC(0)
def light():
     body = "{value: " + str(adc_pin.read()) + "}"
     return response_template % body
# ------------------------------------

pwm_pin = machine.PWM(machine.Pin(13))
dty=500

def pwm():
    pwm_pin.duty(dty) 
    body = "{pwm duty: " + str(dty) + "}"
    return response_template % body 
# ------------------------------------

handlers = {
    'time': time,
    'dummy': dummy,
    'light_on': light_on,
    'light_off': light_off,
    'switch': switch,
    'light': light,
    'pwm': pwm,
    }
# -------------------------------------

def main():
    s = socket.socket()
    ai = socket.getaddrinfo("0.0.0.0", 8080)
    addr = ai[0][-1]

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind(addr)
    s.listen(5)
    print("Listening, connect your browser to http://<this_host>:8080")

    while True:
        sleep(0.5)
        res = s.accept()
        client_s = res[0]
        client_addr = res[1]
        req = client_s.recv(4096)
        print("Request:")
        print(req)

        try:
            path = req.decode().split("\r\n")[0].split(" ")[1]
            handler = handlers[path.strip('/').split('/')[0]]
            response = handler()
        except KeyError:
            response = response_404
        except Exception as e:
            response = response_500
            print(str(e))

        client_s.send(b"\r\n".join([line.encode() for line in response.split("\n")]))

        client_s.close()
        print()
# -------------------------------------
main()

