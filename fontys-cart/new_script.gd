
extends Control

var udp = PacketPeerUDP.new()

func _ready():
	udp.set_dest_address("127.0.0.1", 5005)
	print("UDP ready!")

func _input(event):
	if event is InputEventKey and event.pressed and not event.echo:

		if event.keycode == KEY_A:
			send_command("LEFT")

		elif event.keycode == KEY_D:
			send_command("RIGHT")

		elif event.keycode == KEY_Q:
			send_command("QUIT")

func send_command(command):
	udp.put_packet(command.to_utf8_buffer())
	print("Sent:", command)
