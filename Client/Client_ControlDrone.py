import logging
import socket
import keyboard
import pickle
from Client_GradeReceiveThread import GradeReceiverThread


def forward(horizontalSpeedMultiplier: int = 5):
    data = pickle.dumps([
        "forward",  # direction of movement
        horizontalSpeedMultiplier  # speed multiplier
    ])
    UDPClientSocket.sendto(data, serverAddressPort)
    logger.info("forward sent")


def back(horizontalSpeedMultiplier: int = 5):
    data = pickle.dumps([
        "back",  # direction of movement
        horizontalSpeedMultiplier  # speed multiplier
    ])
    UDPClientSocket.sendto(data, serverAddressPort)
    logger.info("back sent")


def left(horizontalSpeedMultiplier: float = 5):
    data = pickle.dumps([
        "left",  # direction of movement
        horizontalSpeedMultiplier  # speed multiplier
    ])
    UDPClientSocket.sendto(data, serverAddressPort)
    logger.info("left sent")


def right(horizontalSpeedMultiplier: float = 5):
    data = pickle.dumps([
        "right",  # direction of movement
        horizontalSpeedMultiplier  # speed multiplier
    ])
    UDPClientSocket.sendto(data, serverAddressPort)
    logger.info("right sent")


def turnRight(angleToTurn: float = 5):
    data = pickle.dumps([
        "turnRight",  # direction of movement
        angleToTurn  # by how many degrees
    ])
    UDPClientSocket.sendto(data, serverAddressPort)
    logger.info("turnRight sent")


def turnLeft(angleToTurn: float = 5):
    data = pickle.dumps([
        "turnLeft",  # direction of movement
        angleToTurn  # by how many degrees
    ])
    UDPClientSocket.sendto(data, serverAddressPort)
    logger.info("turnLeft sent")


def up(verticalSpeed: float = 2):
    data = pickle.dumps([
        "up",  # direction of movement
        verticalSpeed  # speed
    ])
    UDPClientSocket.sendto(data, serverAddressPort)
    logger.info("up sent")


def down(verticalSpeed: float = 2):
    data = pickle.dumps([
        "down",  # direction of movement
        verticalSpeed  # speed
    ])
    UDPClientSocket.sendto(data, serverAddressPort)
    logger.info("down sent")


def hover():
    data = pickle.dumps([
        "hover"  # direction of movement
    ])
    UDPClientSocket.sendto(data, serverAddressPort)
    logger.info("hover sent")


def goto(x: float, y: float, z: float, velocity: float, hasToFinish: bool):
    data = pickle.dumps([
        "goto",  # direction of movement
        x,  # x destination coordinate
        y,  # y destination coordinate
        z,  # z destination coordinate
        velocity,  # speed of movement
        hasToFinish  # Whether the action should be stoppable while running, or the drone has to get to the specified point until any further movement is performed (True == yes, False == no)
    ])
    UDPClientSocket.sendto(data, serverAddressPort)
    logger.info("goto sent")


def initLogger():
    #  Initiating logger -->
    newLogger = logging.getLogger("clientLogger")
    newLogger.setLevel(logging.DEBUG)
    f_handler = logging.FileHandler('Client.log', 'w', encoding="utf-8")
    logFormat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    f_handler.setFormatter(logFormat)
    newLogger.addHandler(f_handler)  # <--
    newLogger.info("Logging initiated")
    return newLogger


if __name__ == '__main__':
    logger: logging.Logger = initLogger()

    # Sending Hello to server
    msgFromClient = "Hello UDP Server"
    bytesToSend = str.encode(msgFromClient)
    serverAddressPort = ("192.168.1.246", 20001)
    bufferSize = 1024

    # Create a UDP socket at client side
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    gradeReceiverThread = GradeReceiverThread(logger, UDPClientSocket, bufferSize)
    gradeReceiverThread.start()

    # Send to server using created UDP socket
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)

    keyboard.add_hotkey('w', forward, timeout=0)
    keyboard.add_hotkey('s', back, timeout=0)
    keyboard.add_hotkey('a', left, timeout=0)
    keyboard.add_hotkey('d', right, timeout=0)
    keyboard.add_hotkey('e', turnRight, timeout=0)
    keyboard.add_hotkey('q', turnLeft, timeout=0)
    keyboard.add_hotkey('page up', up, timeout=0)
    keyboard.add_hotkey('page down', down, timeout=0)
    keyboard.add_hotkey('space', hover, timeout=0)

    # goto(x=-5.5, y=-5.9, z=-1.1, velocity=5.4, hasToFinish=True)
    # goto function is available but not bound to key

    keyboard.wait('esc')  # wait while esc not pressed

    finishSimMessage = pickle.dumps([
        "finishedSim"
    ])
    UDPClientSocket.sendto(finishSimMessage, serverAddressPort)
    logger.info("finishedSim sent")

    gradeReceiverThread.stop()
    UDPClientSocket.close()
