import json
import logging
import threading
import time

import airsim
import numpy as np
import cv2
import geopy.distance


class Grade(threading.Thread):
    def __init__(self, numberOfAruco: int, clientSocket, clientAddress, logger: logging.Logger, geodeticArucoCoordinates: list, originPosOfAruco: dict, ueIds: dict):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()

        self.client = airsim.MultirotorClient()
        self.clientSocket = clientSocket
        self.clientAddress = clientAddress
        self.logger = logger
        self.geodeticArucoCoordinates = geodeticArucoCoordinates
        self.originPosOfAruco = originPosOfAruco
        self.ueIds = ueIds

        with open("CreatingConfigurationFiles/gradeConfig.json", "r") as file:
            gradeConfig = json.load(file)

        # Params from JSON file
        self.currentPoints: float = gradeConfig["pointsAtStartOfGame"]
        self.gameTime: float = gradeConfig["gameTime"]  # In seconds
        # self.timeForHeatZoneKill: float = gradeConfig["timeForHeatZoneKill"]  # In seconds
        self.pointsForQRDetected: float = gradeConfig["pointsForQRDetected"]  # The number of points the agent receives upon detecting correctly an Aruco QR code

        self.unseenQR = list(range(1, numberOfAruco + 1))
        self.seenQR = []

        self.lastKnownXPos = 0
        self.lastKnownYPos = 0
        self.lastKnownZPos = 0

    def getCurrentGrade(self) -> float:
        return self.currentPoints

    def stop(self):
        """
        Method to be called when the thread should be stopped
        :return: 
        """""
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        while not self.stopped():
            try:
                airsimResponse = self.client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)])[0]  # Get image from Airsim client
                img1d = np.frombuffer(airsimResponse.image_data_uint8, dtype=np.uint8)  # get numpy array
                frame = img1d.reshape((airsimResponse.height, airsimResponse.width, 3))  # reshape array to 4 channel image array H X W X 4
                currPoints = self.grade(frame)
                self.logger.info("The frame was graded. The current grade is: " + str(currPoints))

                self.clientSocket.sendto(str.encode(str(currPoints)), self.clientAddress)
                self.logger.info("The grade was sent to client")
                time.sleep(1)  # Max grades given per second: 1
            except:
                pass

    def grade(self, frame: np.ndarray) -> float:  # TODO: improve and finish grade() func
        arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_1000)
        arucoParams = cv2.aruco.DetectorParameters_create()

        corners, ids, rejected = cv2.aruco.detectMarkers(frame, arucoDict, parameters=arucoParams)

        state = self.client.getMultirotorState()  # Get Airsim state data
        dronePos = state.gps_location  # get GPS coordinates (longitude, latitude, altitude) of drone

        if ids is not None:
            for i in range(len(ids)):
                recognizedId = ids[i][0]  # Selecting the ID of aruco recognized
                if recognizedId in self.unseenQR:
                    distance = geopy.distance.distance((dronePos.latitude,  # Position of drone
                                                        dronePos.longitude),
                                                       (self.geodeticArucoCoordinates[recognizedId - 1][0],  # Position of potentially recognized Aruco code
                                                        self.geodeticArucoCoordinates[recognizedId - 1][1])).m  # In meters
                    self.logger.info("Distance to recognized aruco number " + str(recognizedId) + " is: " + str(distance))
                    if distance <= 30:
                        self.unseenQR.remove(recognizedId)
                        self.seenQR.append(recognizedId)

                        # When Aruco seen, make it disappear -->
                        position = self.client.simGetObjectPose(self.ueIds[str(recognizedId)])  # Get current position of object. needed to keep the format identical
                        position.position.x_val = self.originPosOfAruco["x"]  # Changing location -->
                        position.position.y_val = self.originPosOfAruco["y"]
                        position.position.z_val = self.originPosOfAruco["z"]  # <--
                        self.client.simSetObjectPose(self.ueIds[str(recognizedId)], position)  # Set new location to the "inf" location: origin location of all Aruco codes
                        # <--

                        self.currentPoints += self.pointsForQRDetected

        geoPoint = airsim.GeoPoint()

        # collision = self.client.simGetCollisionInfo()  # Get Airsim collision data

        return self.currentPoints
