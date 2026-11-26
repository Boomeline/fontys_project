import legoeducation as le
import time

# update these values to match the Connection Card
card_color = le.LEGO_COLOR_GREEN
card_serial = '1857'

# Connect to the Double Motor
doublemotor = le.DoubleMotor()
doublemotor.connect(card_color=card_color, card_serial=card_serial)

# Check connection
if not doublemotor.connected:
	print('Error connecting to Double Motor.')
	exit(1) # error connecting

# Print both motor positions for five seconds
for i in range(50):
	print(f"Left Position: {doublemotor.motor[le.MOTOR_LEFT].position}, Right Position: {doublemotor.motor[le.MOTOR_RIGHT].position}")
	time.sleep(0.1)

# Disconnect
doublemotor.disconnect()
exit(0) # successful execution