import threading
import socket
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
        self.client.takeoffAsync().join()  # let drone take-off

        self.UDPServerSocket.sendto(str.encode("Connection Successful"), bytesAddressPair[1])

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
        self.grade = Grade(self.client, self.numOfAruco, self.UDPServerSocket, self.clientAddress)
        self.grade.start()
        while not self.stopped():  # Thread stops upon call to stop() method above
            bytesAddressPair = self.UDPServerSocket.recvfrom(bufferSize)  # Receiving via socket
            commandReceived = bytesAddressPair[0].decode()  # Received data - movement request of drone

            if commandReceived == "forward":
                self.logger.info("Command received: Move Forward")
                pass
            elif commandReceived == "back":
                self.logger.info("Command received: Move Back")
                pass
            elif commandReceived == "up":
                self.logger.info("Command received: Move Up")
                pass
            elif commandReceived == "down":
                self.logger.info("Command received: Move Down")
                pass
            elif commandReceived == "left":
                self.logger.info("Command received: Move Left")
                pass
            elif commandReceived == "right":
                self.logger.info("Command received: Move Right")
                pass
            elif commandReceived == "turn":
                self.logger.info("Command received: Turn by ... degrees")
                pass
            elif commandReceived == "hover":
                self.logger.info("Command received: Hover")
                pass
            else:
                self.logger.error("Command doesn't exist!")

        self.UDPServerSocket.close()
