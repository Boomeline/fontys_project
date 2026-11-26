
import legoeducation as le
import msvcrt

singlemotor = le.SingleMotor()

singlemotor.connect(
    card_color=le.LEGO_COLOR_GREEN,
    card_serial="1857"
)

if not singlemotor.connected:
    print("Error connecting to Single Motor.")
    exit(1)

print("Motor connected!")
print("LEFT ARROW  = +1 degree")
print("RIGHT ARROW = -1 degree")
print("Q = quit")

try:
    while True:
        key = msvcrt.getch()

        # Arrow keys on Windows
        if key in (b'\x00', b'\xe0'):
            arrow = msvcrt.getch()

            if arrow == b'K':  # Left arrow
                singlemotor.motor_run_for_degrees(90)
                print("Motor: +20 degree")

            elif arrow == b'M':  # Right arrow
                singlemotor.motor_run_for_degrees(-90)
                print("Motor: -20 degree")

        elif key.lower() == b'q':
            break

finally:
    singlemotor.disconnect()
    print("Motor disconnected.")
