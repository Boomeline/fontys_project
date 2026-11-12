import cv2

camera = cv2.VideoCapture(1)

aruco = cv2.aruco

dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

parameters = aruco.DetectorParameters()

detector = aruco.ArucoDetector(dictionary, parameters)

while True:
    success, frame = camera.read()

    if not success:
        break

    corners, ids, rejected = detector.detectMarkers(frame)

    if ids is not None:

        aruco.drawDetectedMarkers(frame, corners, ids)

        for i, marker_id in enumerate(ids):

            marker_corners = corners[i][0]

            x1, y1 = marker_corners[0]
            x2, y2 = marker_corners[2]

            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            cv2.circle(
                frame,
                (center_x, center_y),
                5,
                (0, 0, 255),
                -1
            )

            print(
                f"ID: {marker_id} "
                f"X: {center_x} "
                f"Y: {center_y}"
            )
    cv2.imshow("ArUco Tracker", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()