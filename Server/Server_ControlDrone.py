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
        self.logger = None
        self.grade = None
        self.numOfAruco = None
        self.cameraAngleDeg = 0

        # Creating sockets for
        self.UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)  # Create a datagram socket
        self.UDPServerSocket.bind((localIP, localPort))  # Bind to address and ip

        # Initialize Airsim client according to the IP received
        self.client = airsim.MultirotorClient()  # connect to the simulator
        self.client.confirmConnection()
        self.client.reset()
        self.client.enableApiControl(True)  # enable API control on Drone
        self.client.armDisarm(True)  # arm Drone
        time.sleep(1)
        self.client.takeoffAsync().join()  # let drone take-off

        bytesAddressPair = self.UDPServerSocket.recvfrom(bufferSize)  # Receiving "Hello" from client
        self.clientAddressRecv = bytesAddressPair[1]  # socket for receiving commands

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
        :return:
        """
        self.grade = Grade(self.numOfAruco, self.UDPServerSocket, self.clientAddressRecv, self.logger)
        self.grade.start()
        while not self.stopped():  # Thread stops upon call to stop() method above
            try:
                bytesAddressPair = self.UDPServerSocket.recvfrom(bufferSize)  # Receiving via socket
                dataReceived = pickle.loads(bytesAddressPair[0])  # Received data - movement request of drone
                commandReceived = dataReceived[0]

                if commandReceived == "forward":
                    self.logger.info("Command received: Move Forward")
                    horizontalSpeedMultiplier = dataReceived[1]
                    xSpeed = np.cos(np.deg2rad(self.cameraAngleDeg)) * horizontalSpeedMultiplier
                    ySpeed = np.sin(np.deg2rad(self.cameraAngleDeg)) * horizontalSpeedMultiplier
                    zSpeed = 0  # Vertical
                    self.client.moveByVelocityAsync(xSpeed, ySpeed, zSpeed, 1, airsim.DrivetrainType.MaxDegreeOfFreedom,
                                                    airsim.YawMode(False, self.cameraAngleDeg))

                elif commandReceived == "back":
                    self.logger.info("Command received: Move Back")
                    horizontalSpeedMultiplier = dataReceived[1]
                    xSpeed = -np.cos(np.deg2rad(self.cameraAngleDeg)) * horizontalSpeedMultiplier
                    ySpeed = -np.sin(np.deg2rad(self.cameraAngleDeg)) * horizontalSpeedMultiplier
                    zSpeed = 0  # Vertical
                    self.client.moveByVelocityAsync(xSpeed, ySpeed, zSpeed, 1, airsim.DrivetrainType.MaxDegreeOfFreedom,
                                                    airsim.YawMode(False, self.cameraAngleDeg))

                elif commandReceived == "up":
                    self.logger.info("Command received: Move Up")
                    verticalSpeed = dataReceived[1]
                    xSpeed = 0
                    ySpeed = 0
                    zSpeed = -verticalSpeed  # Vertical
                    self.client.moveByVelocityAsync(xSpeed, ySpeed, zSpeed, 0.5, airsim.DrivetrainType.MaxDegreeOfFreedom,
                                                    airsim.YawMode(False, self.cameraAngleDeg))

                elif commandReceived == "down":
                    self.logger.info("Command received: Move Down")
                    verticalSpeed = dataReceived[1]
                    xSpeed = 0
                    ySpeed = 0
                    zSpeed = verticalSpeed  # Vertical
                    self.client.moveByVelocityAsync(xSpeed, ySpeed, zSpeed, 0.5, airsim.DrivetrainType.MaxDegreeOfFreedom,
                                                    airsim.YawMode(False, self.cameraAngleDeg))

                elif commandReceived == "left":
                    self.logger.info("Command received: Move Left")
                    horizontalSpeedMultiplier = dataReceived[1]
                    xSpeed = -np.sin(np.deg2rad(self.cameraAngleDeg)) * horizontalSpeedMultiplier
                    ySpeed = -np.cos(np.deg2rad(self.cameraAngleDeg)) * horizontalSpeedMultiplier
                    zSpeed = 0  # Vertical
                    self.client.moveByVelocityAsync(xSpeed, ySpeed, zSpeed, 1, airsim.DrivetrainType.MaxDegreeOfFreedom,
                                                    airsim.YawMode(False, self.cameraAngleDeg))

                elif commandReceived == "right":
                    self.logger.info("Command received: Move Right")
                    horizontalSpeedMultiplier = dataReceived[1]
                    xSpeed = np.sin(np.deg2rad(self.cameraAngleDeg)) * horizontalSpeedMultiplier
                    ySpeed = np.cos(np.deg2rad(self.cameraAngleDeg)) * horizontalSpeedMultiplier
                    zSpeed = 0  # Vertical
                    self.client.moveByVelocityAsync(xSpeed, ySpeed, zSpeed, 1, airsim.DrivetrainType.MaxDegreeOfFreedom,
                                                    airsim.YawMode(False, self.cameraAngleDeg))

                elif commandReceived == "turnRight":
                    self.logger.info("Command received: Turn right by 5 degrees")
                    anglesToTurn = dataReceived[1]
                    self.cameraAngleDeg += anglesToTurn
                    xSpeed = 0
                    ySpeed = 0
                    zSpeed = 0  # Vertical
                    self.client.moveByVelocityAsync(xSpeed, ySpeed, zSpeed, 1, airsim.DrivetrainType.MaxDegreeOfFreedom,
                                                    airsim.YawMode(False, self.cameraAngleDeg))

                elif commandReceived == "turnLeft":
                    self.logger.info("Command received: Turn left by 5 degrees")
                    anglesToTurn = dataReceived[1]
                    self.cameraAngleDeg -= anglesToTurn
                    xSpeed = 0
                    ySpeed = 0
                    zSpeed = 0  # Vertical
                    self.client.moveByVelocityAsync(xSpeed, ySpeed, zSpeed, 1, airsim.DrivetrainType.MaxDegreeOfFreedom,
                                                    airsim.YawMode(False, self.cameraAngleDeg))

                elif commandReceived == "hover":
                    self.logger.info("Command received: Hover")
                    self.client.hoverAsync()

                elif commandReceived == "goto":
                    self.logger.info("Command received: goto")
                    x = dataReceived[1]  # x destination coordinate
                    y = dataReceived[2]  # y destination coordinate
                    z = dataReceived[3]  # z destination coordinate
                    velocity = dataReceived[4]  # speed of movement
                    hasToFinish = dataReceived[5]  # Whether the action should be stoppable while running
                    if hasToFinish:  # yes
                        self.client.moveToPositionAsync(x, y, z, velocity)
                    else:  # no
                        self.client.moveToPositionAsync(x, y, z, velocity).join()

                elif commandReceived == "finishedSim":
                    self.logger.info("Command received: Finish Simulation")
                    break

                else:
                    self.logger.error("Command doesn't exist!")  # Should never occur
                    self.client.hoverAsync()
            except:
                pass
        self.grade.stop()
        self.UDPServerSocket.close()
