import json
import logging
import socket
import threading
import time

import airsim
import numpy as np
import cv2


class Grade(threading.Thread):
    def __init__(self, numberOfAruco: int, clientSocket, clientAddress, logger: logging.Logger):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()

        # self.client = client
        self.client = airsim.MultirotorClient()
        self.clientSocket = clientSocket
        # self.clientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)  # Create a datagram socket
        # self.clientSocket.bind((localIP, int(localPort) + 1))
        self.clientAddress = clientAddress
        self.logger = logger

        with open("CreatingConfigurationFiles/gradeConfig.json", "r") as file:
            gradeConfig = json.load(file)

        # Params from JSON file
        self.currentPoints: float = gradeConfig["pointsAtStartOfGame"]
        self.gameTime: float = gradeConfig["gameTime"]  # In seconds
        # self.timeForHeatZoneKill: float = gradeConfig["timeForHeatZoneKill"]  # In seconds
        self.pointsForQRDetected: float = gradeConfig["pointsForQRDetected"]  # The number of points the agent receives upon detecting correctly an Aruco QR code

        self.unseenQR = list(range(1, numberOfAruco + 1))
        self.seenQR = []

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
                airsimResponse = self.client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)])[0]
                img1d = np.frombuffer(airsimResponse.image_data_uint8, dtype=np.uint8)  # get numpy array
                frame = img1d.reshape((airsimResponse.height, airsimResponse.width, 3))  # reshape array to 4 channel image array H X W X 4
                currPoints = self.grade(frame)
                self.logger.info("The frame was graded. The current grade is: " + str(currPoints))

                self.clientSocket.sendto(str.encode(str(currPoints)), self.clientAddress)
                self.logger.info("The grade was sent to client")
                time.sleep(1)  # 0.1
            except:
                pass

    def grade(self, frame: np.ndarray) -> float:  # TODO: improve and finish grade() func
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
        try:
            state = self.client.getMultirotorState()  # Get Airsim state data
            collision = self.client.simGetCollisionInfo()  # Get Airsim collision data
        except:
            pass

        return self.currentPoints
