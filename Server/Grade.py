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
    """
    Class to represent the thread which is to handle all grading-related issues of the drone for its reinforcement learning.
    Current functionality:
    1. Giving grade:
        1.1. Handle collisions: Whenever the drone collides with a physical object, it is transported back to where it has been up to 10 seconds before (location updates every 10 seconds),
                one of its "lives" is removed, and some amount of points is deducted. These and other parameters are specified in the json file and from there the information is read.
        1.2. Handle recognising an Aruco code: Whenever a QR code is recognised (from the image as the camera on the drone is seeing it), and is within a given radius from the drone,
                the Aruco code "evaporates" and a number of points is awarded to the drone.
        1.3. Handle being seen by the target (Aruco code): Whenever the drone is in line of sight of the Aruco codes (Airsim API for line-of-sight between two points is used),
                a number of points is deducted from the drone every second where it remains in said line of sight.
    2. Sending the current grade at some rate per second to the client.
    """

    def __init__(self, numberOfAruco: int, clientSocket, clientAddress, logger: logging.Logger, originPosOfAruco: dict, ueIds: dict):
        """
        Constructor of the class. Reads the gradeConfig json file for the needed grading parameters.

        :param numberOfAruco: number of aruco codes available for placing
        :param clientSocket: socket for the final grade to be sent to via UDP
        :param clientAddress: Address of the client for the grade to be sent to
        :param logger: logger to log the needed information
        :param originPosOfAruco: "home" of aruco, where the aruco is placed after being recognised. Used in place of despawning the object
        :param ueIds: IDs of the object in UE4 which are the aruco codes
        :param currentPoints:
        """
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()

        self.client = airsim.MultirotorClient()  # New Airsim client for new thread
        self.clientSocket = clientSocket  # socket to receive the commands from
        self.clientAddress = clientAddress  # address to receive the commands from
        self.logger = logger  # Logger to file
        self.originPosOfAruco = originPosOfAruco  # "Home" position of aruco codes, instead of despawning
        self.ueIds = ueIds  # Ids of Aruco code objects in UE4

        self.timeArucoHeatZoneLastChecked: float = 0  # Time of check if drone in heat zone of aruco
        self.timeLastLocationRecorded: float = 0  # Time of recorded location of drone

        with open("CreatingConfigurationFiles/gradeConfig.json", "r") as file:  # Reading JSON from file
            gradeConfig = json.load(file)

        # Params from JSON file
        self.currentPoints: float = gradeConfig["pointsAtStartOfGame"]
        self.gameTime: float = gradeConfig["gameTime"]  # In seconds
        self.pointsForQRDetected: float = gradeConfig["pointsForQRDetected"]  # The number of points the agent receives upon detecting correctly an Aruco QR code
        self.droneRecognitionRadius: float = gradeConfig["droneRecognitionRadius"]  # Max radius from which the aruco codes are recognized by the drone
        self.heatZoneRadius: float = gradeConfig["heatZoneRadius"]  # Max radius from which the drone is recognized by the aruco codes
        self.minusPointsPerSecInHeatZone: float = gradeConfig["minusPointsPerSecInHeatZone"]  # Number of points deducted per second per aruco
        self.numberOfLives: int = gradeConfig["numberOfLives"]  # Number of lives the drone has before end of simulation
        self.minusPointsForLifeLost = gradeConfig["minusPointsForLifeLost"]  # Number of points deducted for lost life
        self.pointsToFinishSim = gradeConfig["pointsToFinishSim"]  # Minimal amount of points for a sim. Anything below this limit and the simulation ends

        self.unseenQR = list(range(1, numberOfAruco + 1))  # List of ids of unseen QR codes (by the drone)
        self.seenQR = []  # List of ids of seen QR codes (by the drone)

        self.firstCollisionAtStartOfSim = False  # Flag to ignore first collision (at the start of sim)

        self.lastKnowsDroneGPSLoc = self.client.getMultirotorState().gps_location  # Parameter to record the last location recorded for drone (updates every 10 seconds).
        # Used for "jump back" at collision

    def getCurrentGrade(self) -> float:
        """
        returns the current grade of the drone
        :return: Current grade: float
        """
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
        """
        Method to be executed by the thread.
        :return:
        """
        self.timeArucoHeatZoneLastChecked = time.time()  # First update of the time last checked
        while not self.stopped():
            airsimResponse = self.client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)])[0]  # Get image from Airsim client
            img1d = np.frombuffer(airsimResponse.image_data_uint8, dtype=np.uint8)  # get numpy array
            frame = img1d.reshape((airsimResponse.height, airsimResponse.width, 3))  # reshape array to 3 channel image array H x W x 3
            self.grade(frame)  # Grade the frame
            self.logger.info("The frame was graded. The current grade is: " + str(self.currentPoints))  # Logging

            self.clientSocket.sendto(str.encode(str(self.currentPoints)), self.clientAddress)  # Send grade to client
            self.logger.info("The grade was sent to client")  # Logging
            time.sleep(0.2)  # Max grades given per second: 5
        return self.currentPoints  # return current number of points

    def findGPSCoordinatesOfAruco(self, arucoId):
        """
        Given an aruco ID, the method calculates and returns the geodetic coordinates (longitude, latitude, altitude) of the aruco code
        :param arucoId: Id of the desired Aruco code
        :return: 
        """""
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
        """
        Given an aruco ID, the method "despawns" the aruco, meaning transporting the aruco to a closed off room, the location of which is specified as originPosOfAruco.
        This is done after the aruco was recognized by the drone
        :param arucoId: The ID of the aruco code
        :return:
        """
        # When Aruco seen, make it disappear
        position = self.client.simGetObjectPose(self.ueIds[str(arucoId)])  # Get current position of object. needed to keep the format identical
        position.position.x_val = self.originPosOfAruco["x"]  # Changing location -->
        position.position.y_val = self.originPosOfAruco["y"]
        position.position.z_val = self.originPosOfAruco["z"]  # <--
        self.client.simSetObjectPose(self.ueIds[str(arucoId)], position)  # Set new location to the "inf" location: origin location of all Aruco codes

    def handleSeenArucoCodes(self, frame):
        """
        The method handles the occasion when an Aruco code is seen and recognized (within radius) by the drone.
        The method adds the relevant number of points, despawns the aruco, updates the relevant parameters and fields
        :param frame: The frame upon which the Aruco recognition is performed
        :return:
        """
        arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_1000)  # Dictionary used for aruco recognition
        arucoParams = cv2.aruco.DetectorParameters_create()

        corners, ids, rejected = cv2.aruco.detectMarkers(frame, arucoDict, parameters=arucoParams)  # Detect aruco codes in frame

        state = self.client.getMultirotorState()  # Get Airsim state data
        dronePos = state.gps_location  # get GPS coordinates (longitude, latitude, altitude) of drone

        if ids is not None:  # If any Aruco was recognized in the frame
            for i in range(len(ids)):  # For every recognized aruco, check if it exists on the map (in case of misinterpreted pixels in the image)
                recognizedId = ids[i][0]  # Selecting the ID of aruco recognized
                if recognizedId in self.unseenQR:  # If aruco is yet unseen and exists on map
                    gpsCoordinatesOfAruco = self.findGPSCoordinatesOfAruco(recognizedId)  # Get geodetic coordinates of the recognized aruco

                    # Calculating the distance between the aruco and the drone
                    distanceFromDroneToAruco = geopy.distance.distance((dronePos.latitude,  # Position of drone
                                                                        dronePos.longitude),
                                                                       (gpsCoordinatesOfAruco[0],  # Position of potentially recognized Aruco code
                                                                        gpsCoordinatesOfAruco[1])).m  # In meters

                    self.logger.info("Distance to recognized aruco number " + str(recognizedId) + " is: " + str(distanceFromDroneToAruco))  # Logging
                    if distanceFromDroneToAruco <= self.droneRecognitionRadius:  # If recognized aruco is in radius
                        # Updating lists
                        self.unseenQR.remove(recognizedId)
                        self.seenQR.append(recognizedId)

                        self.makeArucoDisappear(recognizedId)  # Despawning the aruco code
                        self.currentPoints += self.pointsForQRDetected  # Adding points to the drone for aruco recognized

    def handleInArucoHeatZone(self):
        """
        The method handles the drone being "seen" by the aruco codes, deducting points per second per aruco.
        :return:
        """
        countMinusPoints = 0  # Counter for number of aruco codes which "can see" the drone and are within radius
        droneGeoPoint = self.client.getMultirotorState().gps_location  # Getting the geodetic coordinates of the current position of the drone

        for arucoIndex in range(len(self.unseenQR)):  # For every aruco, check
            gpsCoordinatesOfAruco = self.findGPSCoordinatesOfAruco(self.unseenQR[arucoIndex])

            geoPointAruco = airsim.GeoPoint()  # Initiating GeoPoint
            geoPointAruco.latitude = gpsCoordinatesOfAruco[0]  # Updating GeoPoint -->
            geoPointAruco.longitude = gpsCoordinatesOfAruco[1]
            geoPointAruco.altitude = gpsCoordinatesOfAruco[2]  # <--

            # Calculating the distance between aruco and drone
            distanceFromDroneToAruco = geopy.distance.distance((droneGeoPoint.latitude,  # Position of drone
                                                                droneGeoPoint.longitude),
                                                               (gpsCoordinatesOfAruco[0],  # Position of potentially recognized Aruco code
                                                                gpsCoordinatesOfAruco[1])).m  # In meters
            if time.time() - self.timeArucoHeatZoneLastChecked >= 1 and \
                    distanceFromDroneToAruco <= self.heatZoneRadius and \
                    self.client.simTestLineOfSightBetweenPoints(geoPointAruco, droneGeoPoint):
                # if checks: more than 1 second has passed since last check; distance from drone to aruco is within radius; drone in line of sight of aruco
                countMinusPoints += 1  # Increase count of how many Arucos
                self.logger.info("drone in range of aruco number:" + str(self.unseenQR[arucoIndex]) + " heat zone")  # Logging

        if countMinusPoints > 0:  # If any aruco is seeing the drone
            self.logger.info("Time since last grade: " + str(time.time() - self.timeArucoHeatZoneLastChecked) + " seconds")  # Logging
            self.currentPoints -= (self.minusPointsPerSecInHeatZone * countMinusPoints)  # Deducting the appropriate number of points
            self.timeArucoHeatZoneLastChecked = time.time()  # Recording current time

    def handleCollisions(self):
        """
        The method handles collisions of the drone with any and all physical objects. If drone collides with any object, it loses a life, a certain amount of points is deducted
        and the drone is transported back in time to where it was before the collision.
        :return:
        """
        if time.time() - self.timeLastLocationRecorded >= 10:  # If more than 10 seconds passed
            self.lastKnowsDroneGPSLoc = self.client.getMultirotorState().gps_location  # record the current position of drone
            self.timeLastLocationRecorded = time.time()  # Record time

        collision = self.client.simGetCollisionInfo()  # Get Airsim collision data
        if collision.has_collided and self.firstCollisionAtStartOfSim:  # If drone has collided and the first collision has already occurred
            self.timeLastLocationRecorded = time.time()  # Record time
            self.numberOfLives -= 1  # Deduct life
            self.currentPoints -= self.minusPointsForLifeLost  # Deduct points

            self.logger.info("The drone has collided! Number of \"lives\" left: " + str(self.numberOfLives) + ". The current grade is: " + str(self.currentPoints))  # Logging
            if self.numberOfLives == 0:  # If no lives remaining
                self.stop()  # Quit simulation after relevant actions

            originGPSCoordinates = self.client.getHomeGeoPoint()  # Get spawn point of the drone (at start of simulation)

            # Transform GPS coordinates to ENU (NED in different order) coordinate system (the one Airsim uses)
            currentDroneCoordinates = pm.geodetic2enu(self.lastKnowsDroneGPSLoc.latitude,
                                                      self.lastKnowsDroneGPSLoc.longitude,
                                                      self.lastKnowsDroneGPSLoc.altitude,
                                                      originGPSCoordinates.latitude,
                                                      originGPSCoordinates.longitude,
                                                      originGPSCoordinates.altitude)

            # Initialize position to teleport to (back in time up to 10 seconds) -->
            oldDronePos = self.client.simGetVehiclePose()
            oldDronePos.position.x_val = currentDroneCoordinates[1]
            oldDronePos.position.y_val = currentDroneCoordinates[0]
            oldDronePos.position.z_val = -currentDroneCoordinates[2]  # <--

            self.client.simSetVehiclePose(oldDronePos, True)  # Set new position of the drone
            self.client.hoverAsync().join()  # Stop any action that was performed and hover in place
        else:  # If this is first collision
            self.firstCollisionAtStartOfSim = True  # Specify first collision occurred

    def grade(self, frame: np.ndarray) -> None:
        self.handleSeenArucoCodes(frame)  # Handle seen aruco codes
        self.handleInArucoHeatZone()  # Handle the drone being in heat zone of aruco codes
        self.handleCollisions()  # Handle drone collisions

        if self.currentPoints <= self.pointsToFinishSim:  # If current points are less than the lower bound of points
            self.stop()  # Stop thread after proper actions
