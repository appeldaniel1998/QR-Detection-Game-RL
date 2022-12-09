import threading
import logging
import airsim
from ArucoCode import ArucoCode


class DynamicMap(threading.Thread):
    """
    A Thread class to handle the logging of the program to file
    """

    def __init__(self, arucos: list[ArucoCode], logger: logging.Logger):
        """
        :param: arucos: list of arucos to modify their location
        :param: logger: logger to log any needed information to file
        """
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()

        self.arucos: list[ArucoCode] = arucos
        self.fullArucoList: list[ArucoCode] = arucos
        self.moveBy: int = 5  # speed of aruco movement
        self.logger: logging.Logger = logger

        self.logger.info("Dynamic map initiated")  # Logging

        self.client = airsim.MultirotorClient()  # Initiating new Airsim client for the thread (client cannot be called simultaneously from 2 threads)
        ArucoCode.airsimClient = self.client  # set the Airsim client to the ArucoCode class

    def stop(self):
        """
        Method to be called when the thread should be stopped
        :return:
        """
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        """
        Method to be executed by the thread.
        :return:
        """
        while not self.stopped():  # Thread stops upon call to stop() method above
            for i in range(len(self.arucos)-1):  # For every item in the arucos list
                arucoCurrPose = self.client.simGetObjectPose(ArucoCode.ueIds[str(self.fullArucoList[i].arucoId)])
                if 16100 <= (arucoCurrPose.position.x_val * 100) + ArucoCode.playerStartPos[0] <= 17450 and \
                        -6200 <= (arucoCurrPose.position.y_val * 100) + ArucoCode.playerStartPos[1] <= -4850 and \
                        50 <= (arucoCurrPose.position.z_val * -100) + ArucoCode.playerStartPos[2] <= 550:
                    # The if statement checks whether the Aruco is in its starter position (was recognized, hence shouldn't be moved from now on, hence it is removed from the list
                    self.arucos.pop(i)  # Remove object from list
                    i -= 1  # Correcting the index of the for loop
                else:
                    self.arucos[i].move(self.moveBy)  # Move Aruco according to its conditions
