
import socket
import legoeducation as le

# -------------------------
# UDP CONNECTION
# -------------------------

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("127.0.0.1", 5005))

print("Waiting for Godot commands...")

# -------------------------
# LEGO CONNECTION
# -------------------------

card_color = le.LEGO_COLOR_GREEN
card_serial = "1857"

doublemotor = le.DoubleMotor()

doublemotor.connect(
    card_color=card_color,
    card_serial=card_serial
)

if not doublemotor.connected:
    print("Error connecting to Double Motor.")
    sock.close()
    exit(1)

print("LEGO Double Motor connected!")
print("Waiting for commands from Godot...")

# -------------------------
# COMMAND HANDLING
# -------------------------

try:
    while True:

        data, address = sock.recvfrom(1024)
        command = data.decode("utf-8").strip().upper()

        print("Received:", command)

        if command == "LEFT":

            doublemotor.motor_run_for_degrees(
                -90,
                motor=le.MOTOR_LEFT
            )

            print("Left motor: 90 degrees")

        elif command == "RIGHT":

            doublemotor.motor_run_for_degrees(
                90,
                motor=le.MOTOR_RIGHT
            )

            print("Right motor: 90 degrees")

        elif command == "QUIT":

            print("Shutting down...")
            break

        else:
            print("Unknown command:", command)

finally:
    doublemotor.disconnect()
    sock.close()
    print("Disconnected. Goodbye!")
