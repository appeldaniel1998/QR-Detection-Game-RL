import airsim
from CreateMap import createMap
import logging
from LoggerThread import LoggerThread
from Server_ControlDrone import ServerThread

# TODO fix or dismiss the following bugs
"""
Known bugs:
1. Sometimes, while flying, the axis change mid flight and the "left" and "right" controls dont work as expected
2. Sometimes, the drone starts with 1 collision and -50 points - FIXED by ignoring 1st collision
"""

if __name__ == '__main__':
    serverThread = ServerThread()  # Initiating connection to clientPC

    client: airsim.MultirotorClient = serverThread.client
    loggerThread = LoggerThread(client, "Server")  # Initiate logger class instance
    logger: logging.Logger = loggerThread.getLogger()  # Getting logger from the loggerThread instance
    serverThread.logger = logger  # Assignment of logger to server thread (to be able to log from it to the same file and with the same settings)
    logger.info("Connected to instance of Airsim")  # Logging

    client, numOfArucoOnMap, originPosOfAruco, ueIds, dynamicMapThread = createMap(client, logger)  # Creating map

    # Updating the serverThread parameters returned by the createMap method
    serverThread.numOfAruco = numOfArucoOnMap
    serverThread.originPosOfAruco = originPosOfAruco
    serverThread.ueIds = ueIds

    logger.info("Simulation ready to start...\n")  # Logging

    loggerThread.start()  # Starting continuous logging of Airsim data to file and console
    serverThread.start()  # Start continuous receiving of commands to the drone

    # Stopping threads
    serverThread.join()
    loggerThread.stop()
    dynamicMapThread.stop()

