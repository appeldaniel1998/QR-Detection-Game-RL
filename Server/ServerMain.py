import airsim
from CreateMap import createMap
import logging
from LoggerThread import LoggerThread
from Server_ControlDrone import ServerThread
from Grade import Grade

if __name__ == '__main__':
    serverThread = ServerThread()  # Initiating connection to clientPC

    client: airsim.MultirotorClient = serverThread.client
    loggerThread = LoggerThread(client, "Server")  # Initiate logger class instance
    logger: logging.Logger = loggerThread.getLogger()  # Getting logger from the loggerThread instance
    serverThread.logger = logger  # Assignment of logger to server thread (to be able to log from it to the same file and with the same settings)
    logger.info("Connected to instance of Airsim")  # Logging

    client, numOfArucoOnMap, geodeticArucoCoordinates, originPosOfAruco, ueIds = createMap(client, logger)
    serverThread.numOfAruco = numOfArucoOnMap
    serverThread.geodeticArucoCoordinates = geodeticArucoCoordinates
    serverThread.originPosOfAruco = originPosOfAruco
    serverThread.ueIds = ueIds

    logger.info("Simulation ready to start...\n")  # Logging

    # loggerThread.start()  # Starting continuous logging of Airsim data to file and console
    serverThread.start()  # Start continuous receiving of commands to the drone

    serverThread.join()
    # loggerThread.stop()






    # client.simSetObjectMaterialFromTexture("testCube1_2", "C:/Users/appel/PycharmProjects/AirsimSimulation/ArucoImages/aruco1.jpg")

