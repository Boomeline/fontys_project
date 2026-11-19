
extends Node2D

var udp := PacketPeerUDP.new()

var robot_position := Vector2.ZERO
var robot_id := -1
var marker_detected := false

var camera_width := 640.0
var camera_height := 480.0

func _ready():
	var result = udp.bind(4242)

	if result == OK:
		print("Listening for Python data on port 4242!")
	else:
		print("Could not bind UDP port 4242. Error: ", result)

func _process(_delta):
	# Read all incoming UDP packets
	while udp.get_available_packet_count() > 0:
		var packet = udp.get_packet()
		var message = packet.get_string_from_utf8()

		var data = JSON.parse_string(message)

		if data is Dictionary:

			# Receive camera dimensions
			if data.has("width") and data.has("height"):
				camera_width = float(data["width"])
				camera_height = float(data["height"])

			# Check whether a marker was detected
			if data.has("x") and data["x"] != null:
				robot_id = int(data["id"])

				var screen_size = get_viewport_rect().size

				robot_position = Vector2(
					float(data["x"]) * screen_size.x / camera_width,
					float(data["y"]) * screen_size.y / camera_height
				)

				marker_detected = true
			else:
				marker_detected = false

			queue_redraw()


func _draw():
	if marker_detected:
		draw_circle(robot_position, 15, Color.GREEN)

		draw_string(
			ThemeDB.fallback_font,
			Vector2(20, 30),
			"Robot ID: " + str(robot_id)
		)
	else:
		draw_string(
			ThemeDB.fallback_font,
			Vector2(20, 30),
            "No marker detected"
		)
