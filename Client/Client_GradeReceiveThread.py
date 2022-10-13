import socket
import threading
import time
import logging


class GradeReceiverThread(threading.Thread):
    """
    A Thread class to handle the logging of the program to file
    """

    def __init__(self, logger: logging.Logger, UDPClientSocket: socket.socket, bufferSize: int = 1024):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        self.UDPClientSocket = UDPClientSocket
        self.bufferSize = bufferSize
        self.grades = []
        self.logger = logger

        self.logger.info("Grade receiving initiated")

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
        Method to be executed by the thread. Continuous receiving of grades from server
        :return:
        """
        while not self.stopped():  # Thread stops upon call to stop() method above
            bytesAddressPair = self.UDPClientSocket.recvfrom(self.bufferSize)
            grade = float(bytesAddressPair[0].decode())
            self.logger.info("Grade received: " + str(grade))
            self.grades.append(grade)
