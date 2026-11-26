             
import socket

# Maak een UDP-verbinding
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Luister op poort 5005
sock.bind(("127.0.0.1", 5005))

print("Python wacht op commando's...")

while True:
    data, address = sock.recvfrom(1024)

    command = data.decode("utf-8")

    print("Ontvangen:", command)
