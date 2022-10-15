import json
import logging
import threading
import time

import airsim
import numpy as np
import cv2
import geopy.distance
import pymap3d as pm


class Grade(threading.Thread):
    def __init__(self, numberOfAruco: int, clientSocket, clientAddress, logger: logging.Logger, originPosOfAruco: dict, ueIds: dict, currentPoints: float = -1):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()

        self.client = airsim.MultirotorClient()
        self.clientSocket = clientSocket
        self.clientAddress = clientAddress
        self.logger = logger
        self.originPosOfAruco = originPosOfAruco
        self.ueIds = ueIds

        self.timeArucoHeatZoneLastChecked: float = 0
        self.timeLastLocationRecorded: float = 0

        with open("CreatingConfigurationFiles/gradeConfig.json", "r") as file:
            gradeConfig = json.load(file)

        # Params from JSON file
        if currentPoints == -1:
            self.currentPoints: float = gradeConfig["pointsAtStartOfGame"]
        else:
            self.currentPoints: float = currentPoints
        self.gameTime: float = gradeConfig["gameTime"]  # In seconds
        self.pointsForQRDetected: float = gradeConfig["pointsForQRDetected"]  # The number of points the agent receives upon detecting correctly an Aruco QR code
        self.droneRecognitionRadius: float = gradeConfig["droneRecognitionRadius"]
        self.heatZoneRadius: float = gradeConfig["heatZoneRadius"]
        self.minusPointsPerSecInHeatZone: float = gradeConfig["minusPointsPerSecInHeatZone"]
        self.numberOfLives: int = gradeConfig["numberOfLives"]
        self.minusPointsForLifeLost = gradeConfig["minusPointsForLifeLost"]
        self.pointsToFinishSim = gradeConfig["pointsToFinishSim"]

        self.unseenQR = list(range(1, numberOfAruco + 1))
        self.seenQR = []

        self.lastKnowsDroneGPSLoc = self.client.getMultirotorState().gps_location

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
        self.timeArucoHeatZoneLastChecked = time.time()
        while not self.stopped():
            airsimResponse = self.client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)])[0]  # Get image from Airsim client
            img1d = np.frombuffer(airsimResponse.image_data_uint8, dtype=np.uint8)  # get numpy array
            frame = img1d.reshape((airsimResponse.height, airsimResponse.width, 3))  # reshape array to 4 channel image array H X W X 4
            self.grade(frame)
            self.logger.info("The frame was graded. The current grade is: " + str(self.currentPoints))

            self.clientSocket.sendto(str.encode(str(self.currentPoints)), self.clientAddress)
            self.logger.info("The grade was sent to client")
            time.sleep(0.2)  # Max grades given per second: 5
        return self.currentPoints

    def findGPSCoordinatesOfAruco(self, arucoId):
        pos = self.client.simGetObjectPose(self.ueIds[str(arucoId)])
        originGPSCoordinates = self.client.getHomeGeoPoint()

        # Converting Airsim coordinate system to GPS coordinates
        gpsCoordinatesOfAruco = pm.enu2geodetic(pos.position.y_val,
                                                pos.position.x_val,
                                                -pos.position.z_val,
                                                originGPSCoordinates.latitude,
                                                originGPSCoordinates.longitude,
                                                originGPSCoordinates.altitude)
        return gpsCoordinatesOfAruco

    def makeArucoDisappear(self, arucoId):
        # When Aruco seen, make it disappear
        position = self.client.simGetObjectPose(self.ueIds[str(arucoId)])  # Get current position of object. needed to keep the format identical
        position.position.x_val = self.originPosOfAruco["x"]  # Changing location -->
        position.position.y_val = self.originPosOfAruco["y"]
        position.position.z_val = self.originPosOfAruco["z"]  # <--
        self.client.simSetObjectPose(self.ueIds[str(arucoId)], position)  # Set new location to the "inf" location: origin location of all Aruco codes

    def handleSeenArucoCodes(self, frame):
        arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_1000)
        arucoParams = cv2.aruco.DetectorParameters_create()

        corners, ids, rejected = cv2.aruco.detectMarkers(frame, arucoDict, parameters=arucoParams)

        state = self.client.getMultirotorState()  # Get Airsim state data
        dronePos = state.gps_location  # get GPS coordinates (longitude, latitude, altitude) of drone

        if ids is not None:
            for i in range(len(ids)):
                recognizedId = ids[i][0]  # Selecting the ID of aruco recognized
                if recognizedId in self.unseenQR:
                    gpsCoordinatesOfAruco = self.findGPSCoordinatesOfAruco(recognizedId)
                    distanceFromDroneToAruco = geopy.distance.distance((dronePos.latitude,  # Position of drone
                                                                        dronePos.longitude),
                                                                       (gpsCoordinatesOfAruco[0],  # Position of potentially recognized Aruco code
                                                                        gpsCoordinatesOfAruco[1])).m  # In meters
                    self.logger.info("Distance to recognized aruco number " + str(recognizedId) + " is: " + str(distanceFromDroneToAruco))
                    if distanceFromDroneToAruco <= self.droneRecognitionRadius:
                        self.unseenQR.remove(recognizedId)
                        self.seenQR.append(recognizedId)
                        self.makeArucoDisappear(recognizedId)
                        self.currentPoints += self.pointsForQRDetected

    def handleInArucoHeatZone(self):
        countMinusPoints = 0
        for arucoIndex in range(len(self.unseenQR)):
            gpsCoordinatesOfAruco = self.findGPSCoordinatesOfAruco(self.unseenQR[arucoIndex])
            geoPointAruco = airsim.GeoPoint()
            geoPointAruco.latitude = gpsCoordinatesOfAruco[0]
            geoPointAruco.longitude = gpsCoordinatesOfAruco[1]
            geoPointAruco.altitude = gpsCoordinatesOfAruco[2]
            droneGeoPoint = self.client.getMultirotorState().gps_location
            distanceFromDroneToAruco = geopy.distance.distance((droneGeoPoint.latitude,  # Position of drone
                                                                droneGeoPoint.longitude),
                                                               (gpsCoordinatesOfAruco[0],  # Position of potentially recognized Aruco code
                                                                gpsCoordinatesOfAruco[1])).m  # In meters
            if time.time() - self.timeArucoHeatZoneLastChecked >= 1 and \
                    distanceFromDroneToAruco <= self.heatZoneRadius and \
                    self.client.simTestLineOfSightBetweenPoints(geoPointAruco, droneGeoPoint):
                # if checks: more than 1 second has passed since last check; distance from drone to aruco is within radius; drone in line of sight of aruco
                countMinusPoints += 1  # Increase count of how many Arucos
                self.logger.info("drone in range of aruco number:" + str(self.unseenQR[arucoIndex]) + " heat zone")

        if countMinusPoints > 0:
            self.logger.info("Time since last grade: " + str(time.time() - self.timeArucoHeatZoneLastChecked) + " seconds")
            self.currentPoints -= (self.minusPointsPerSecInHeatZone * countMinusPoints)
            self.timeArucoHeatZoneLastChecked = time.time()

    def handleCollisions(self):
        if time.time() - self.timeLastLocationRecorded >= 10:
            self.lastKnowsDroneGPSLoc = self.client.getMultirotorState().gps_location
            self.timeLastLocationRecorded = time.time()

        collision = self.client.simGetCollisionInfo()  # Get Airsim collision data
        if collision.has_collided:
            self.timeLastLocationRecorded = time.time()
            self.numberOfLives -= 1
            self.currentPoints -= self.minusPointsForLifeLost

            self.logger.info("The drone has collided! Number of \"lives\" left: " + str(self.numberOfLives) + ". The current grade is: " + str(self.currentPoints))
            if self.numberOfLives == 0:
                self.stop()

            originGPSCoordinates = self.client.getHomeGeoPoint()

            # Transform GPS coordinates to ENU (NED in different order) coordinate system (the one Airsim uses)
            currentDroneCoordinates = pm.geodetic2enu(self.lastKnowsDroneGPSLoc.latitude,
                                                      self.lastKnowsDroneGPSLoc.longitude,
                                                      self.lastKnowsDroneGPSLoc.altitude,
                                                      originGPSCoordinates.latitude,
                                                      originGPSCoordinates.longitude,
                                                      originGPSCoordinates.altitude)

            # Initialize position to teleport to (back in time 5 seconds) -->
            oldDronePos = self.client.simGetVehiclePose()
            oldDronePos.position.x_val = currentDroneCoordinates[1]
            oldDronePos.position.y_val = currentDroneCoordinates[0]
            oldDronePos.position.z_val = -currentDroneCoordinates[2]  # <--

            self.client.simSetVehiclePose(oldDronePos, True)
            self.client.hoverAsync().join()

    def grade(self, frame: np.ndarray) -> None:
        self.handleSeenArucoCodes(frame)
        self.handleInArucoHeatZone()
        self.handleCollisions()

        if self.pointsToFinishSim >= self.currentPoints:
            self.stop()
