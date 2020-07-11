# This code controls a DC motor speed and direction over Wifi using
# Nodemcu esp8266 and L293D motor driver.
# http://localhost:8080/motor_control is the homepage for DC motor control.
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
from time import sleep
from machine import Pin

# set up the pins of nodeMCU and L293D
# 1. We use GPIN 12 and 13 of nodeMCU as output control pins.
# GPIO12 and 13 is connected to the INPUT Pin 2 and 7 of L293D.
# Pin2 = 0 Pin7 = 0 ---> motor off
# Pin2 = 1 Pin7 = 0 ---> motor forward
# Pin2 = 0 Pin7 = 1 ---> motor backward
out1 = Pin(12, Pin.OUT)
out2 = Pin(13, Pin.OUT)

# 2. We use GPID14 of nodeMCU to send the PWM signal to control the speed of motor.
# GPID14 of nodeMCU is connected to the enable 1,2 (Pin 1) of L293D.
pwm = Pin(14)
pwm = machine.PWM(pwm)
pwm.duty(1023)

# 3. We use Analog input pin A0 to connect a transducer to change the speed of
# the motor.
adc = machine.ADC(0)

home_page_str = """
<!DOCTYPE HTML>
<html>
<h1 align=center>NodeMCU DC motor control over WiFi</h1><br><br>
<br><br>
<a href=\"http://192.168.1.168:8080/motor_on\"><button> Motor On </button></a>
<a href=\"http://192.168.1.168:8080/motor_off\"><button> Motor Off </button></a>
<a href=\"http://192.168.1.168:8080/motor_forward\"><button> Motor Forward </button></a>
<a href=\"http://192.168.1.168:8080/motor_backward\"><button> Motor Backward </button></a>
<br>
<br>
<a href=\"http://192.168.1.168:8080/duty_25\"><button> Duty Cycle 25% </button></a>
<a href=\"http://192.168.1.168:8080/duty_50\"><button> Duty Cycle 50% </button></a>
<a href=\"http://192.168.1.168:8080/duty_75\"><button> Duty Cycle 75% </button></a>
<a href=\"http://192.168.1.168:8080/duty_100\"><button> Duty Cycle 100% </button></a>
<br>
<br>
<a href=\"http://192.168.1.168:8080/duty_100\"><button> Stepless Speed Control</button></a>
<br>
<br>
<br>
"""
# create homepage veiw function.
def home_page():
    body = home_page_str + '</html>'
    return response_template % body

# create a motor on view function.
def motor_on():
    out1.value(1)
    out2.value(0)
    pwm.duty(1023)
    body = home_page_str + '<p> Motor is on</p> </html>'
    return response_template % body

# create a motor off view function.
def motor_off():
    out1.value(0)
    out2.value(0)
    body = home_page_str + 'Motor is stopped.'
    return response_template % body

# create a motor forward veiw function.
def motor_forward():
    out1.value(0)
    out2.value(0)
    sleep(3)
    out1.value(1)
    out2.value(0)
    #pwm.duty(1023)
    body = home_page_str + 'Motor rotating in forward direction.'
    return response_template % body

# create a motor backward veiw function.
def motor_backward():
    out1.value(0)
    out2.value(0)
    sleep(3)
    out1.value(0)
    out2.value(1)
    #pwm.duty(1023)
    body = home_page_str + 'Motor rotating in backward direction.'
    return response_template % body

# create PWM duty cycle = 25 veiw function.
def duty_25():
    pwm.duty(255)
    body = home_page_str + 'PWM duty cycle 25%.'
    return response_template % body

# create PWM duty cycle = 50 veiw function.
def duty_50():
    pwm.duty(512)
    body = home_page_str + 'PWM duty cycle 50%.'
    return response_template % body

# create PWM duty cycle = 75 veiw function.
def duty_75():
    pwm.duty(767)
    body = home_page_str + 'PWM duty cycle 75%.'
    return response_template % body

# create PWM duty cycle = 100 veiw function.
def duty_100():
    pwm.duty(1023)
    body = home_page_str + 'PWM duty cycle 100%.'
    return response_template % body

# create analog input duty cycle veiw function.
def analog_duty():
    motor_duty_cycle = adc.read()
    pwm.duty(motor_duty_cycle)
    body = home_page_str + 'PWM duty cycle {}'.format(motor_duty_cycle)
    return response_template % body

# routing dictionary for different view functions.
handlers = {
    'motor_control': home_page,
    'motor_on': motor_on,
    'motor_off': motor_off,
    'motor_forward': motor_forward,
    'motor_backward': motor_backward,
    'duty_100': duty_100,
    'duty_75': duty_75,
    'duty_50': duty_50,
    'duty_25': duty_25,
    'analog_duty': analog_duty,
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
        sleep(.5)
        print("Before accept:")
        res = s.accept()
        print("After accept:")
        client_s = res[0]
        client_addr = res[1]
        req = client_s.recv(4096)
        print("Request:")
        print(req)

        # This first line of a request looks like "GET /arbitrary/path/ HTTP/1.1 "
        # It has three parts and seperated by a space char (' ').
        # So the first part is the GET method, second is the path, the third is the
        # HTTP version used. We only need the second part.
        # The first line of a request is: req.decode().split('\r\n')[0]
        # The second part of first line is:
        # req.decode().split('\r\n')[0].split(" ")[1]
        try:
            path = req.decode().split('\r\n')[0].split(' ')[1]
            # http://localhost:8080/motor_control is the homepage.
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
