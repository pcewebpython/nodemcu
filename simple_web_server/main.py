try:
    import usocket as socket
except:
    import socket

response_404 = """HTTP/1.0 404 NOT FOUND

<h1>404 Not Found</h1>
"""

response_template = """HTTP/1.0 200 OK

%s
"""
import machine
import ntptime, utime
from machine import RTC
seconds = ntptime.time()
rtc = RTC()
rtc.datetime(utime.localtime(seconds))

adc = machine.ADC(0)

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

handlers = {
    'time': time,
    'dummy': dummy,
}

def main():
    s = socket.socket()
    ai = socket.getaddrinfo("0.0.0.0", 8080)
    addr = ai[0][-1]

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind(addr)
    s.listen(5)
    print("Listening, connect your browser to http://<this_host>:8080/")

    while True:
        res = s.accept()
        client_s = res[0]
        client_addr = res[1]
        req = client_s.recv(4096)
        print("Request:")
        print(req)

        # The first line of a request looks like "GET /arbitrary/path/ HTTP/1.1".
        # This grabs that first line and whittles it down to just "/arbitrary/path/"
        path = req.decode().split("\r\n")[0].split(" ")[1]

        try:
            # Given the path, identify the correct handler to use
            handler = handlers[path.strip('/').split('/')[0]]
            response = handler()
        except KeyError:
            response = 404_response

        # A handler returns an entire response in the form of a multi-line string.
        # This breaks up the response into single strings, byte-encodes them, and
        # joins them back together with b"\r\n". Then it sends that to the client.
        client_s.send(b"\r\n".join([line.encode() for line in response.split("\n")]))

        client_s.close()
        print()

main()
