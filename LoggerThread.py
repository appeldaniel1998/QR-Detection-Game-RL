import threading
import time
import logging


class LoggerThread(threading.Thread):
    """
    A Thread class to handle the logging of the program to file
    """

    def __init__(self, client):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        self.client = client

        #  Initiating logger -->
        self.logger = logging.getLogger("mainLogger")
        self.logger.setLevel(logging.DEBUG)
        f_handler = logging.FileHandler('controlAPI.log', 'w', encoding="utf-8")
        logFormat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        f_handler.setFormatter(logFormat)
        self.logger.addHandler(f_handler)  # <--

        self.logger.info("Logging initiated")

    def stop(self):
        """
        Method to be called when the thread should be stopped
        :return: 
        """""
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        """
        Method to be executed be the thread. Logs info from Airsim
        :return:
        """
        while not self.stopped():  # Thread stops upon call to stop() method above
            state = self.client.getMultirotorState()
            collision = self.client.simGetCollisionInfo()
            self.logger.info("State:\n" + str(state))
            self.logger.info("Collision:\n" + str(collision))
            time.sleep(1)

    def getLogger(self):
        """
        Simple getter method to allow logging from outside the class
        :return: logger
        """
        return self.logger
