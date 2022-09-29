import threading
import time

import airsim
from CreateMap import createMap
import numpy as np
import logging
from LoggerThread import LoggerThread


if __name__ == '__main__':
    # init airsim and drones
    client = airsim.MultirotorClient()  # connect to the simulator
    client.confirmConnection()
    client.reset()

    loggerThread = LoggerThread(client)  # Initiate logger class instance
    logger = loggerThread.getLogger()  # Getting logger from the loggerThread instance
    logger.info("Connected to instance of Airsim")  # Logging

    client = createMap(client)
    logger.info("Created map")  # Logging

    client.enableApiControl(True)  # enable API control on Drone0
    client.armDisarm(True)  # arm Drone

    logger.info("Simulation ready to start...\n")  # Logging

    loggerThread.start()  # Starting continuous logging of Airsim data to file and console
    #  Init complete

    """..........................."""

    time.sleep(5)
    loggerThread.stop()

    # client.simSetObjectMaterialFromTexture("testCube1_2", "C:/Users/appel/PycharmProjects/pythonProject6/ArucoImages/aruco1.jpg")

    # client.takeoffAsync().join()  # let Drone0 take-off
    # client.moveToPositionAsync(0, 0, -1, 1).join()
    # client.hoverAsync().join()
    #
    # xSpeed = 0
    # ySpeed = 5
    # zSpeed = 0  # Vertical
    # camera_heading = 180
    # client.moveByVelocityAsync(xSpeed, ySpeed, zSpeed, 1, airsim.DrivetrainType.MaxDegreeOfFreedom,
    #                            airsim.YawMode(False, camera_heading)).join()
    # client.hoverAsync().join()
    #
    # state = client.getMultirotorState()
    # print(state)
    #
    # collision = client.simGetCollisionInfo()
    # print(collision)
