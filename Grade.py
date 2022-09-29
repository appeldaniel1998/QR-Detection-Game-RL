import json
import airsim
import numpy as np
import cv2


class Grade:
    def __init__(self, client: airsim.MultirotorClient, numberOfAruco: int):
        self.client = client

        with open("CreatingConfigurationFiles/gradeConfig.json", "r") as file:
            gradeConfig = json.load(file)
        # Params from JSON file
        self.pointsAtStartOfGame: float = gradeConfig["pointsAtStartOfGame"]
        self.gameTime: float = gradeConfig["gameTime"]  # In seconds
        self.timeForHeatZoneKill: float = gradeConfig["timeForHeatZoneKill"]  # In seconds
        self.pointsForQRDetected: float = gradeConfig["pointsForQRDetected"]  # The number of points the agent receives upon detecting correctly an Aruco QR code

        self.currentPoints = self.pointsAtStartOfGame
        self.unseenQR = list(range(1, numberOfAruco + 1))
        self.seenQR = []

    def getCurrentGrade(self) -> float:
        return self.currentPoints

    def grade(self, frame: np.ndarray) -> None:
        arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_1000)
        arucoParams = cv2.aruco.DetectorParameters_create()

        corners, ids, rejected = cv2.aruco.detectMarkers(frame, arucoDict, parameters=arucoParams)

        if ids is not None:
            for i in range(len(ids)):
                recognizedId = ids[i][0]
                if recognizedId in self.unseenQR:
                    self.unseenQR.remove(recognizedId)
                    self.seenQR.append(recognizedId)
                    self.currentPoints += self.pointsForQRDetected

        state = self.client.getMultirotorState()
