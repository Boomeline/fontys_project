
import legoeducation as le
import msvcrt

# Connection Card
card_color = le.LEGO_COLOR_GREEN
card_serial = "1857"

# Connect to the Double Motor
doublemotor = le.DoubleMotor()
doublemotor.connect(
    card_color=card_color,
    card_serial=card_serial
)

if not doublemotor.connected:
    print("Error connecting to Double Motor.")
    exit(1)

print("LEGO Double Motor connected!")
print("A = Left motor: 90 degrees")
print("D = Right motor: 90 degrees")
print("Q = Disconnect and quit")

try:
    while True:
        key = msvcrt.getwch().lower()

        if key == "a":
            doublemotor.motor_run_for_degrees(
                -90,
                motor=le.MOTOR_LEFT
            )
            print("Left motor: 90 degrees")

        elif key == "d":
            doublemotor.motor_run_for_degrees(
                90,
                motor=le.MOTOR_RIGHT
            )
            print("Right motor: 90 degrees")

        elif key == "q":
            print("Shutting down...")
            break

finally:
    doublemotor.disconnect()
    print("Disconnected. Goodbye!")

