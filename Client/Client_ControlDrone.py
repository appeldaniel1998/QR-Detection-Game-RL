import logging
import socket
import keyboard
import pickle


def forward():
    UDPClientSocket.sendto(str.encode("forward"), serverAddressPort)
    logger.info("forward sent")


def back():
    UDPClientSocket.sendto(str.encode("back"), serverAddressPort)
    logger.info("back sent")


def left():
    UDPClientSocket.sendto(str.encode("left"), serverAddressPort)
    logger.info("left sent")


def right():
    UDPClientSocket.sendto(str.encode("right"), serverAddressPort)
    logger.info("right sent")


def turnRight():
    UDPClientSocket.sendto(str.encode("turnRight"), serverAddressPort)
    logger.info("turnRight sent")


def turnLeft():
    UDPClientSocket.sendto(str.encode("turnLeft"), serverAddressPort)
    logger.info("turnLeft sent")


def up():
    UDPClientSocket.sendto(str.encode("up"), serverAddressPort)
    logger.info("up sent")


def down():
    UDPClientSocket.sendto(str.encode("down"), serverAddressPort)
    logger.info("down sent")


def hover():
    UDPClientSocket.sendto(str.encode("hover"), serverAddressPort)
    logger.info("hover sent")


if __name__ == '__main__':
    #  Initiating logger -->
    logger = logging.getLogger("clientLogger")
    logger.setLevel(logging.DEBUG)
    f_handler = logging.FileHandler('Client.log', 'w', encoding="utf-8")
    logFormat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    f_handler.setFormatter(logFormat)
    logger.addHandler(f_handler)  # <--
    logger.info("Logging initiated")

    msgFromClient = "Hello UDP Server"
    bytesToSend = str.encode(msgFromClient)
    serverAddressPort = ("192.168.1.246", 20001)
    bufferSize = 1024

    # Create a UDP socket at client side
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Send to server using created UDP socket
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    # msgFromServer = UDPClientSocket.recvfrom(bufferSize)  # Receiving that the connection was successful and the client is permitted to start sending commands to drone
    # msg = "Message from Server: {}".format(msgFromServer[0])
    # print(msg)

    keyboard.add_hotkey('w', forward, timeout=0)
    keyboard.add_hotkey('s', back, timeout=0)
    keyboard.add_hotkey('a', left, timeout=0)
    keyboard.add_hotkey('d', right, timeout=0)
    keyboard.add_hotkey('e', turnRight, timeout=0)
    keyboard.add_hotkey('q', turnLeft, timeout=0)
    keyboard.add_hotkey('page up', up, timeout=0)
    keyboard.add_hotkey('page down', down, timeout=0)
    keyboard.add_hotkey('space', hover, timeout=0)

    keyboard.wait()  # infinite wait
