import airsim
from CreateMap import createMap
import logging
from LoggerThread import LoggerThread
from Server_ControlDrone import ServerThread
from Grade import Grade

if __name__ == '__main__':
    serverThread = ServerThread()  # Initiating connection to clientPC

    client: airsim.MultirotorClient = serverThread.client
    loggerThread = LoggerThread(client)  # Initiate logger class instance
    logger: logging.Logger = loggerThread.getLogger()  # Getting logger from the loggerThread instance
    serverThread.logger = logger  # Assignment of logger to server thread (to be able to log from it to the same file and with the same settings)
    logger.info("Connected to instance of Airsim")  # Logging

    # client, numOfArucoOnMap = createMap(client, logger)
    #
    # grade = Grade(client, numOfArucoOnMap)
    # serverThread.grade = grade

    logger.info("Simulation ready to start...\n")  # Logging

    loggerThread.start()  # Starting continuous logging of Airsim data to file and console
    serverThread.start()
    #  Init complete

    """..........................."""

    serverThread.join()
    loggerThread.stop()

    # client.simSetObjectMaterialFromTexture("testCube1_2", "C:/Users/appel/PycharmProjects/AirsimSimulation/ArucoImages/aruco1.jpg")

    # client.takeoffAsync().join()  # let drone take-off
    # client.moveToPositionAsync(0, 0, -1, 1).join()
    # client.hoverAsync().join()
    #
