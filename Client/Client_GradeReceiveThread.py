import socket
import threading
import time
import logging


class GradeReceiverThread(threading.Thread):
    """
    A Thread class to handle receiving grades from the server
    """

    def __init__(self, logger: logging.Logger, UDPClientSocket: socket.socket, bufferSize: int = 1024):
        """
        Initializing thread.

        :param: logger: initialized logging.Logger object ready for logging
        :param: UDPClientSocket: Initialized socket to receive the grades from
        :param: bufferSize: buffer size of the transport between client and server
        """

        threading.Thread.__init__(self)
        self._stop_event = threading.Event()  # safe thread initialization

        self.UDPClientSocket = UDPClientSocket  # Socket to receive the grades from
        self.bufferSize = bufferSize  # buffer size of the transport between client and server
        self.grades = []  # the list of grades to be updated whenever a grade is received
        self.logger = logger  # Logger to log changes to file

        self.logger.info("Grade receiving initiated")  # Logging

        self.reconnectionTries = 0  # number of reconnection tries to server (after 5 tries the program stops)

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
        Method to be executed by the thread. Continuous receiving of grades from server

        :return:
        """
        while not self.stopped():  # Thread stops upon call to stop() method above
            try:  # trying to receive grades from server
                bytesAddressPair = self.UDPClientSocket.recvfrom(self.bufferSize)  # tuple received: data and address
                grade = float(bytesAddressPair[0].decode())  # decoding message received (grade)
                self.logger.info("Grade received: " + str(grade))  # Logging grade received
                self.grades.append(grade)  # appending to list of grades
            except:  # retrying receiving grades
                self.reconnectionTries += 1
                if self.reconnectionTries >= 5:
                    self.stop()
                else:
                    time.sleep(2)
