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

led = machine.Pin(9, machine.Pin.OUT)

def light_on():
    led.value(1)
    body = "You turned the light on!"
    return response_template % body

def light_off():
    led.value(0)
    body = "You turned the light off!"
    return response_template % body

def switch():
    body = "{{state:{}}}".format(machine.Pin(10, machine.Pin.IN).value())
    return response_template % body

adc = machine.ADC(0)

def light():
    body = "{{value:{}}}".format(adc.read())
    return response_template % body

pwm = machine.Pin(13)
pwm = machine.PWM(pwm)
pwm.duty(1024)

def bright():
    pwm.duty(0)
    body = "The LED is bright."
    return response_template % body

def medium_bright():
    pwm.duty(500)
    body = "The LED is medium brightness."
    return response_template % body

def dim():
    pwm.duty(1000)
    body = "The LED is dim."
    return response_template % body

handlers = {
    'time': time,
    'dummy': dummy,
    'light_on': light_on,
    'light_off': light_off,
    'switch': switch,
    'light': light,
    'bright': bright,
    'medium_bright': medium_bright,
    'dim': dim,
}

def main():
    s = socket.socket()
    ai = socket.getaddrinfo("0.0.0.0", 8080)
    addr = ai[0][-1]

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind(addr)
    s.listen(5)
    print("Listening, connect your browser to http://<this_host>:8080")

    while True:
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

main()
