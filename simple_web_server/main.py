try:
    import usocket as socket
except:
    import socket

response_template = """HTTP/1.0 200 OK

%s
"""
import machine
import ntptime, utime
from machine import RTC
from time import sleep

rtc = RTC()
try:
    seconds = ntptime.time()
except:
    seconds = 0
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

def main():
    s = socket.socket()
    ai = socket.getaddrinfo("0.0.0.0", 8080)
    addr = ai[0][-1]

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind(addr)
    s.listen(5)
    print("Listening, connect your browser to http://<this_host>:8080/")

    while True:
        sleep(.5)
        res = s.accept()
        client_s = res[0]
        client_addr = res[1]
        req = client_s.recv(4096)
        print("Request:")
        print(req)

        response = time()

        client_s.send(b"\r\n".join([line.encode() for line in response.split("\n")]))

        client_s.close()
        print()

main()
