import threading
import time
import logging

import airsim

from ArucoCode import ArucoCode


class DynamicMap(threading.Thread):
    """
    A Thread class to handle the logging of the program to file
    """

    def __init__(self, arucos: list[ArucoCode], logger: logging.Logger):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()

        self.arucos: list[ArucoCode] = arucos
        self.moveBy: int = 5
        self.logger: logging.Logger = logger
        self.logger.info("Dynamic map initiated")

        self.client = airsim.MultirotorClient()
        ArucoCode.airsimClient = self.client

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
            for i in range(len(self.arucos)):
                arucoCurrPose = self.client.simGetObjectPose(ArucoCode.ueIds[str(self.arucos[i].arucoId)])
                if 16100 <= (arucoCurrPose.position.x_val * 100) + ArucoCode.playerStartPos[0] <= 17450 and \
                        -6200 <= (arucoCurrPose.position.y_val * 100) + ArucoCode.playerStartPos[1] <= -4850 and \
                        50 <= (arucoCurrPose.position.z_val * -100) + ArucoCode.playerStartPos[2] <= 550:
                    self.arucos.pop(i)
                    i -= 1
                self.arucos[i].move(self.moveBy)
