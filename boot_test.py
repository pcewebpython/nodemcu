import time

try:
    with open("passwords.txt") as f:
        connections = f.readlines()
except OSError:
    print("No passwords.txt file!")
    connections = []


for connection in connections:
    station, password = connection.split("_")

    print("Connecting to {}.".format(station))
    print("password to {}.".format(password))

    for i in range(15):
        print(".")

    time.sleep(1)
