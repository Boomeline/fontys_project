import cv2


class Track ():
    def __init__(self):
        self.width = 640
        self.height = 480
        self.camera = cv2.VideoCapture(1)
        # self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        # self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.aruco = cv2.aruco
        self.dictionary = self.aruco.getPredefinedDictionary(self.aruco.DICT_4X4_50)
        self.parameters = self.aruco.DetectorParameters()
        self.detector = self.aruco.ArucoDetector(self.dictionary, self.parameters)
        self.marker_corners = None

    def cam(self):
    
        success, frame = self.camera.read()

        if not success:
            return None, None, None

        corners, ids, rejected = self.detector.detectMarkers(frame)
        if ids is None:
            return None, None, None

        corners, ids, rejected = self.detector.detectMarkers(frame)

        if ids is not None:

            self.aruco.drawDetectedMarkers(frame, corners, ids)

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

                return (marker_id, center_x, center_y)           
