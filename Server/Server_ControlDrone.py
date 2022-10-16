import logging
import threading
import socket
import time

import airsim
import numpy as np

from Grade import Grade
from Parameters import *
import pickle


# localIP = "192.168.1.246"
# localPort = 20001


class ServerThread(threading.Thread):
    """
    A Thread class to handle connection to client PC on local network, receive commands from it and move the drone accordingly

    The assumption is that ONLY ONE client is trying to connect concurrently

    Operating sequence:
    1. Waits for a client from local network to connect.
    1.1. The client wishing to connect should already have an Airsim simulation game running on his PC
    2. When receives "Hello", initializes an Airsim client connection with the sender's IP address and default
    Airsim port (no input parameter needed for port)
    3.1. Get images continuously from Airsim, calculate grade for each, send the grade back to client
    3.2. The client may, at any point, send movement requests to server

    * 3.1 and 3.2 are run on 2 separate threads
    """

    def __init__(self):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()

        # Empty params to be filled later
        self.logger = None  # Logger
        self.grade = None  # Grade thread
        self.numOfAruco = None  # number of aruco codes
        self.originPosOfAruco = None  # despawn point of aruco
        self.ueIds = None  # IDs of aruco codes in UE4 (list)

        # Creating sockets for
        self.UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)  # Create a datagram socket
        self.UDPServerSocket.bind((localIP, localPort))  # Bind to address and ip

        # Initialize Airsim client according to the IP received
        self.client = airsim.MultirotorClient()  # connect to the simulator
        self.client.confirmConnection()
        self.client.reset()  # Reset drone to default (starting) location
        self.client.enableApiControl(True)  # enable API control on Drone
        self.client.armDisarm(True)  # arm Drone
        time.sleep(1)
        self.client.takeoffAsync().join()  # let drone take-off

        bytesAddressPair = self.UDPServerSocket.recvfrom(bufferSize)  # Receiving "Hello" from client
        self.clientAddressRecv = bytesAddressPair[1]  # socket for receiving commands

        self.cameraAngleDeg = 0  # current angle of the drone

    def stop(self):
        """
        Method to be called when the thread should be stopped
        :return:
        """
        self.grade.stop()
        self.UDPServerSocket.close()
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        """
        Method to be executed by the thread.
        Starts the grading thread and continuously receiving commands from client
        :return:
        """
        self.grade = Grade(self.numOfAruco, self.UDPServerSocket, self.clientAddressRecv, self.logger, self.originPosOfAruco, self.ueIds)  # Initializing grade thread
        self.grade.start()  # Starting the Grade thread

        while not self.stopped():  # Thread stops upon call to stop() method above
            if not self.grade.is_alive():  # If grading was stopped
                break

            try:
                bytesAddressPair = self.UDPServerSocket.recvfrom(bufferSize)  # Receiving via socket
                dataReceived = pickle.loads(bytesAddressPair[0])  # Received data - movement request of drone + decoding message
                commandReceived = dataReceived[0]  # The command received (without parameters of the command)

                if commandReceived == "forward":
                    self.logger.info("Command received: Move Forward")  # Logging
                    horizontalSpeedMultiplier = dataReceived[1]  # Vector speed of the movement (decoded)
                    xSpeed = np.cos(np.deg2rad(self.cameraAngleDeg)) * horizontalSpeedMultiplier  # Calculating the x and y components of the vector of speed
                    ySpeed = np.sin(np.deg2rad(self.cameraAngleDeg)) * horizontalSpeedMultiplier
                    zSpeed = 0  # Vertical
                    self.client.moveByVelocityAsync(xSpeed, ySpeed, zSpeed, 1, airsim.DrivetrainType.MaxDegreeOfFreedom,
                                                    airsim.YawMode(False, self.cameraAngleDeg))  # Sending command to Airsim client

                elif commandReceived == "back":
                    self.logger.info("Command received: Move Back")  # Logging
                    horizontalSpeedMultiplier = dataReceived[1]  # Vector speed of the movement (decoded)
                    xSpeed = -np.cos(np.deg2rad(self.cameraAngleDeg)) * horizontalSpeedMultiplier  # Calculating the x and y components of the vector of speed
                    ySpeed = -np.sin(np.deg2rad(self.cameraAngleDeg)) * horizontalSpeedMultiplier
                    zSpeed = 0  # Vertical
                    self.client.moveByVelocityAsync(xSpeed, ySpeed, zSpeed, 1, airsim.DrivetrainType.MaxDegreeOfFreedom,
                                                    airsim.YawMode(False, self.cameraAngleDeg))  # Sending command to Airsim client

                elif commandReceived == "left":
                    self.logger.info("Command received: Move Left")  # Logging
                    horizontalSpeedMultiplier = dataReceived[1]  # Vector speed of the movement (decoded)
                    xSpeed = -np.sin(np.deg2rad(self.cameraAngleDeg)) * horizontalSpeedMultiplier  # Calculating the x and y components of the vector of speed
                    ySpeed = -np.cos(np.deg2rad(self.cameraAngleDeg)) * horizontalSpeedMultiplier
                    zSpeed = 0  # Vertical
                    self.client.moveByVelocityAsync(xSpeed, ySpeed, zSpeed, 1, airsim.DrivetrainType.MaxDegreeOfFreedom,
                                                    airsim.YawMode(False, self.cameraAngleDeg))  # Sending command to Airsim client

                elif commandReceived == "right":
                    self.logger.info("Command received: Move Right")  # Logging
                    horizontalSpeedMultiplier = dataReceived[1]  # Vector speed of the movement (decoded)
                    xSpeed = np.sin(np.deg2rad(self.cameraAngleDeg)) * horizontalSpeedMultiplier  # Calculating the x and y components of the vector of speed
                    ySpeed = np.cos(np.deg2rad(self.cameraAngleDeg)) * horizontalSpeedMultiplier
                    zSpeed = 0  # Vertical
                    self.client.moveByVelocityAsync(xSpeed, ySpeed, zSpeed, 1, airsim.DrivetrainType.MaxDegreeOfFreedom,
                                                    airsim.YawMode(False, self.cameraAngleDeg))  # Sending command to Airsim client

                elif commandReceived == "up":
                    self.logger.info("Command received: Move Up")  # Logging
                    verticalSpeed = dataReceived[1]  # Vertical speed of the movement (decoded)
                    xSpeed = 0
                    ySpeed = 0
                    zSpeed = -verticalSpeed  # Vertical
                    self.client.moveByVelocityAsync(xSpeed, ySpeed, zSpeed, 0.5, airsim.DrivetrainType.MaxDegreeOfFreedom,
                                                    airsim.YawMode(False, self.cameraAngleDeg))  # Sending command to Airsim client

                elif commandReceived == "down":
                    self.logger.info("Command received: Move Down")  # Logging
                    verticalSpeed = dataReceived[1]  # Vertical speed of the movement (decoded)
                    xSpeed = 0
                    ySpeed = 0
                    zSpeed = verticalSpeed  # Vertical
                    self.client.moveByVelocityAsync(xSpeed, ySpeed, zSpeed, 0.5, airsim.DrivetrainType.MaxDegreeOfFreedom,
                                                    airsim.YawMode(False, self.cameraAngleDeg))  # Sending command to Airsim client

                elif commandReceived == "turnRight":
                    self.logger.info("Command received: Turn right")  # Logging
                    anglesToTurn = dataReceived[1]  # Degrees to turn (decoded)
                    self.cameraAngleDeg += anglesToTurn  # Updating current angle
                    xSpeed = 0
                    ySpeed = 0
                    zSpeed = 0  # Vertical
                    self.client.moveByVelocityAsync(xSpeed, ySpeed, zSpeed, 1, airsim.DrivetrainType.MaxDegreeOfFreedom,
                                                    airsim.YawMode(False, self.cameraAngleDeg))  # Sending command to Airsim client

                elif commandReceived == "turnLeft":
                    self.logger.info("Command received: Turn left")  # Logging
                    anglesToTurn = dataReceived[1]  # Degrees to turn (decoded)
                    self.cameraAngleDeg -= anglesToTurn  # Updating current angle
                    xSpeed = 0
                    ySpeed = 0
                    zSpeed = 0  # Vertical
                    self.client.moveByVelocityAsync(xSpeed, ySpeed, zSpeed, 1, airsim.DrivetrainType.MaxDegreeOfFreedom,
                                                    airsim.YawMode(False, self.cameraAngleDeg))  # Sending command to Airsim client

                elif commandReceived == "hover":
                    self.logger.info("Command received: Hover")  # Logging
                    self.client.hoverAsync()  # Hover

                elif commandReceived == "goto":
                    self.logger.info("Command received: goto")  # Logging
                    x = dataReceived[1]  # x destination coordinate
                    y = dataReceived[2]  # y destination coordinate
                    z = dataReceived[3]  # z destination coordinate
                    velocity = dataReceived[4]  # speed of movement
                    hasToFinish = dataReceived[5]  # Whether the action should be stoppable while running
                    if hasToFinish:  # yes
                        self.client.moveToPositionAsync(x, y, z, velocity).join()  # Sending command to Airsim client
                    else:  # no
                        self.client.moveToPositionAsync(x, y, z, velocity)  # Sending command to Airsim client

                elif commandReceived == "finishedSim":
                    self.logger.info("Command received: Finish Simulation")  # Logging
                    break

                else:
                    self.logger.error("Command doesn't exist!")  # Should never occur
                    self.client.hoverAsync()  # Hover
            except:
                pass

            if not self.grade.is_alive():
                break

        if self.grade.is_alive():  # If thread is alive, stop it
            self.grade.stop()

        self.UDPServerSocket.close()  # Closing socket
