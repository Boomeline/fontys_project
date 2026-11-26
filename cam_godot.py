import cv2
import socket
import json

# UDP connection
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

GODOT_ADDRESS = ("127.0.0.1", 4242)

width = 640
height = 480
camera = cv2.VideoCapture(0)
# camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
# camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
aruco = cv2.aruco
dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters()
detector = aruco.ArucoDetector(dictionary, parameters)
marker_corners = None

data = {
"width": str(width),
"height": str(height),
}

message = json.dumps(data).encode("utf-8")

sock.sendto(message, GODOT_ADDRESS)

print("active")

while True:
    success, frame = camera.read()

    if not success:
        continue

    corners, ids, rejected = detector.detectMarkers(frame)

    if ids is not None:

        aruco.drawDetectedMarkers(frame, corners, ids)

        for i, marker_id in enumerate(ids):

            marker_corners = corners[i][0]

            x1, y1 = marker_corners[0]
            x2, y2 = marker_corners[2]

            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            data = {
                "id": int(marker_id),
                 "x": center_x,
                 "y": center_y
            }
    
    message = json.dumps(data).encode("utf-8")
    sock.sendto(message, GODOT_ADDRESS)

            
