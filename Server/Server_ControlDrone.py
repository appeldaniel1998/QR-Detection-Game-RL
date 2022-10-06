import threading
import socket
import time

import airsim
import numpy as np

from Grade import Grade

localIP = "192.168.1.246"
localPort = 20001
bufferSize = 1024


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

        # connecting to Airsim
        self.UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)  # Create a datagram socket
        self.UDPServerSocket.bind((localIP, localPort))  # Bind to address and ip

        bytesAddressPair = self.UDPServerSocket.recvfrom(bufferSize)  # Receiving "Hello" from client
        self.clientAddress = bytesAddressPair[1]
        ipAddress = self.clientAddress[0]

        # Initialize Airsim client according to the IP received
        self.client = airsim.MultirotorClient(ip=str(ipAddress))  # connect to the simulator
        self.client.confirmConnection()
        self.client.reset()
        self.client.enableApiControl(True)  # enable API control on Drone
        self.client.armDisarm(True)  # arm Drone
        time.sleep(0.3)
        self.client.takeoffAsync().join()  # let drone take-off

        # self.UDPServerSocket.sendto(str.encode("Connection Successful"), bytesAddressPair[1])

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
        # self.grade = Grade(self.client, self.numOfAruco, self.UDPServerSocket, self.clientAddress)
        # self.grade.start()
        while not self.stopped():  # Thread stops upon call to stop() method above
            bytesAddressPair = self.UDPServerSocket.recvfrom(bufferSize)  # Receiving via socket
            commandReceived = bytesAddressPair[0].decode()  # Received data - movement request of drone

            if commandReceived == "forward":
                self.logger.info("Command received: Move Forward")
                xSpeed = np.cos(np.deg2rad(self.cameraAngleDeg)) * 5
                ySpeed = np.sin(np.deg2rad(self.cameraAngleDeg)) * 5
                zSpeed = 0  # Vertical
                self.client.moveByVelocityAsync(xSpeed, ySpeed, zSpeed, 1, airsim.DrivetrainType.MaxDegreeOfFreedom,
                                                airsim.YawMode(False, self.cameraAngleDeg))#.join()

            elif commandReceived == "back":
                self.logger.info("Command received: Move Back")
                xSpeed = -np.cos(np.deg2rad(self.cameraAngleDeg)) * 5
                ySpeed = -np.sin(np.deg2rad(self.cameraAngleDeg)) * 5
                zSpeed = 0  # Vertical
                self.client.moveByVelocityAsync(xSpeed, ySpeed, zSpeed, 1, airsim.DrivetrainType.MaxDegreeOfFreedom,
                                                airsim.YawMode(False, self.cameraAngleDeg))#.join()

            elif commandReceived == "up":
                self.logger.info("Command received: Move Up")
                xSpeed = 0
                ySpeed = 0
                zSpeed = -2  # Vertical
                self.client.moveByVelocityAsync(xSpeed, ySpeed, zSpeed, 0.5, airsim.DrivetrainType.MaxDegreeOfFreedom,
                                                airsim.YawMode(False, self.cameraAngleDeg))#.join()

            elif commandReceived == "down":
                self.logger.info("Command received: Move Down")
                xSpeed = 0
                ySpeed = 0
                zSpeed = 2  # Vertical
                self.client.moveByVelocityAsync(xSpeed, ySpeed, zSpeed, 0.5, airsim.DrivetrainType.MaxDegreeOfFreedom,
                                                airsim.YawMode(False, self.cameraAngleDeg))#.join()

            elif commandReceived == "left":
                self.logger.info("Command received: Move Left")
                xSpeed = -np.sin(np.deg2rad(self.cameraAngleDeg)) * 5
                ySpeed = -np.cos(np.deg2rad(self.cameraAngleDeg)) * 5
                zSpeed = 0  # Vertical
                self.client.moveByVelocityAsync(xSpeed, ySpeed, zSpeed, 1, airsim.DrivetrainType.MaxDegreeOfFreedom,
                                                airsim.YawMode(False, self.cameraAngleDeg))#.join()

            elif commandReceived == "right":
                self.logger.info("Command received: Move Right")
                xSpeed = np.sin(np.deg2rad(self.cameraAngleDeg)) * 5
                ySpeed = np.cos(np.deg2rad(self.cameraAngleDeg)) * 5
                zSpeed = 0  # Vertical
                self.client.moveByVelocityAsync(xSpeed, ySpeed, zSpeed, 1, airsim.DrivetrainType.MaxDegreeOfFreedom,
                                                airsim.YawMode(False, self.cameraAngleDeg))#.join()

            elif commandReceived == "turnRight":
                self.logger.info("Command received: Turn right by 5 degrees")  # TODO
                self.cameraAngleDeg += 5
                xSpeed = 0
                ySpeed = 0
                zSpeed = 0  # Vertical
                self.client.moveByVelocityAsync(xSpeed, ySpeed, zSpeed, 1, airsim.DrivetrainType.MaxDegreeOfFreedom,
                                                airsim.YawMode(False, self.cameraAngleDeg))#.join()

            elif commandReceived == "turnLeft":
                self.logger.info("Command received: Turn left by 5 degrees")  # TODO
                self.cameraAngleDeg -= 5
                xSpeed = 0
                ySpeed = 0
                zSpeed = 0  # Vertical
                self.client.moveByVelocityAsync(xSpeed, ySpeed, zSpeed, 1, airsim.DrivetrainType.MaxDegreeOfFreedom,
                                                airsim.YawMode(False, self.cameraAngleDeg))#.join()

            elif commandReceived == "hover":
                self.logger.info("Command received: Hover")
                self.client.hoverAsync()#.join()

            else:
                self.logger.error("Command doesn't exist!")
                self.client.hoverAsync()

        self.UDPServerSocket.close()
