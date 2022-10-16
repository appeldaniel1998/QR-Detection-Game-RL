import logging
import socket
import time
import keyboard
import pickle
from Client_GradeReceiveThread import GradeReceiverThread
from Parameters import *


def forward(horizontalSpeedMultiplier: int = 5):
    """
    Command drone to move forward from current position.
    The function sends an appropriate message to the server via a UDP socket and logs a message

    :param: horizontalSpeedMultiplier: float: default: 5. Vector length of the velocity of movement of the drone forward (increase for faster movement, decrease for slower)
    :return:
    """
    data = pickle.dumps([  # encode object for sending
        "forward",  # direction of movement
        horizontalSpeedMultiplier  # speed multiplier
    ])
    UDPSocketSend.sendto(data, serverAddressPortSend)  # Send
    logger.info("forward sent")  # Logging


def back(horizontalSpeedMultiplier: int = 5):
    """
    Command drone to move back from current position.
    The function sends an appropriate message to the server via a UDP socket and logs a message

    :param: horizontalSpeedMultiplier: float: default: 5. Vector length of the velocity of movement of the drone backwards (increase for faster movement, decrease for slower)
    :return:
    """
    data = pickle.dumps([  # encode object for sending
        "back",  # direction of movement
        horizontalSpeedMultiplier  # speed multiplier
    ])
    UDPSocketSend.sendto(data, serverAddressPortSend)  # Send
    logger.info("back sent")  # Logging


def left(horizontalSpeedMultiplier: float = 5):
    """
    Command drone to move left from current position.
    The function sends an appropriate message to the server via a UDP socket and logs a message

    :param: horizontalSpeedMultiplier: float: default: 5. Vector length of the velocity of movement of the drone to the left (increase for faster movement, decrease for slower)
    :return:
    """
    data = pickle.dumps([  # encode object for sending
        "left",  # direction of movement
        horizontalSpeedMultiplier  # speed multiplier
    ])
    UDPSocketSend.sendto(data, serverAddressPortSend)  # Send
    logger.info("left sent")  # Logging


def right(horizontalSpeedMultiplier: float = 5):
    """
    Command drone to move right from current position.
    The function sends an appropriate message to the server via a UDP socket and logs a message

    :param: horizontalSpeedMultiplier: float: default: 5. Vector length of the velocity of movement of the drone to the right (increase for faster movement, decrease for slower)
    :return:
    """
    data = pickle.dumps([  # encode object for sending
        "right",  # direction of movement
        horizontalSpeedMultiplier  # speed multiplier
    ])
    UDPSocketSend.sendto(data, serverAddressPortSend)  # Send
    logger.info("right sent")  # Logging


def turnRight(angleToTurn: float = 5):
    """
    Command drone to turn right from current position.
    The function sends an appropriate message to the server via a UDP socket and logs a message

    :param: angleToTurn: float: default: 5. Amount of degrees (the angle) to turn right from the current orientation.
            Note: The drone turns in the direction closest to its current orientation, i.e. if the command is to turn right 200 degrees, the drone will turn 160 degrees left.
            Note: the command lasts for up to 1 second, so for larger values (closer to 180), the command may not finish execution, in which case the angle will correct itself
                whenever the next command is issued.
    :return:
    """
    data = pickle.dumps([  # encode object for sending
        "turnRight",  # direction of movement
        angleToTurn  # by how many degrees
    ])
    UDPSocketSend.sendto(data, serverAddressPortSend)  # Send
    logger.info("turnRight sent")  # Logging


def turnLeft(angleToTurn: float = 5):
    """
    Command drone to turn left from current position.
    The function sends an appropriate message to the server via a UDP socket and logs a message

    :param: angleToTurn: float: default: 5. Amount of degrees (the angle) to turn left from the current orientation.
            Note: The drone turns in the direction closest to its current orientation, i.e. if the command is to turn left 200 degrees, the drone will turn 160 degrees right.
            Note: the command lasts for up to 1 second, so for larger values (closer to 180), the command may not finish execution, in which case the angle will correct itself
                whenever the next command is issued.
    :return:
    """
    data = pickle.dumps([  # encode object for sending
        "turnLeft",  # direction of movement
        angleToTurn  # by how many degrees
    ])
    UDPSocketSend.sendto(data, serverAddressPortSend)  # Send
    logger.info("turnLeft sent")  # Logging


def up(verticalSpeed: float = 2):
    """
    Command drone to move up from current position.
    The function sends an appropriate message to the server via a UDP socket and logs a message

    :param: verticalSpeed: float: default: 2. Velocity of movement of the drone upwards (increase for faster movement, decrease for slower)
    :return:
    """
    data = pickle.dumps([  # encode object for sending
        "up",  # direction of movement
        verticalSpeed  # speed
    ])
    UDPSocketSend.sendto(data, serverAddressPortSend)  # Send
    logger.info("up sent")  # Logging


def down(verticalSpeed: float = 2):
    """
    Command drone to move down from current position.
    The function sends an appropriate message to the server via a UDP socket and logs a message

    :param: verticalSpeed: float: default: 2. Velocity of movement of the drone downwards (increase for faster movement, decrease for slower)
    :return:
    """
    data = pickle.dumps([  # encode object for sending
        "down",  # direction of movement
        verticalSpeed  # speed
    ])
    UDPSocketSend.sendto(data, serverAddressPortSend)  # Send
    logger.info("down sent")  # Logging


def hover():
    """
    Command drone to hover in place.
    The function sends an appropriate message to the server via a UDP socket and logs a message

    Note: Due to Airsim physics, hovering after fast or long movements results in the drone moving around in circles

    :return:
    """
    data = pickle.dumps([  # encode object for sending
        "hover"  # direction of movement
    ])
    UDPSocketSend.sendto(data, serverAddressPortSend)  # Send
    logger.info("hover sent")  # Logging


def goto(x: float, y: float, z: float, velocity: float, hasToFinish: bool = True):
    """
    Command for the drone to go to a specified location (via x, y, z coordinates) in a straight line with no regard to objects in the way.
    The function sends an appropriate message to the server via a UDP socket and logs a message

    :param: x: float: destination X coordinate
    :param: y: float: destination Y coordinate
    :param: z: float: destination Z coordinate
    :param: velocity: float: velocity of the drone while flying to its destination
    :param: hasToFinish: boolean: default: True. Specifies whether the action should be stoppable (by sending a different command) (True = unstoppable, False = stoppable)
    :return:
    """
    data = pickle.dumps([  # encode object for sending
        "goto",  # direction of movement
        x,  # x destination coordinate
        y,  # y destination coordinate
        z,  # z destination coordinate
        velocity,  # speed of movement
        hasToFinish  # Whether the action should be stoppable while running, or the drone has to get to the specified point until any further movement is performed (True == yes, False == no)
    ])
    UDPSocketSend.sendto(data, serverAddressPortSend)  # Send
    logger.info("goto sent")  # Logging


def finishExecution():
    """
    Method to update a value in order for the execution of the program to stop (sends a "finish simulation" method to server, stops the running thread and exits the program
    :return:
    """
    global finishExec
    finishExec = True


def initLogger():
    """
    Initialization procedure of the logger. Logs to file.

    :return: created logger (logging.Logger)
    """
    #  Initiating logger -->
    newLogger = logging.getLogger("clientLogger")
    newLogger.setLevel(logging.DEBUG)  # Log every message (from the lowest level of importance)
    f_handler = logging.FileHandler('Client.log', 'w', encoding="utf-8")  # destination file path to and encoding
    logFormat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # Format of message
    f_handler.setFormatter(logFormat)
    newLogger.addHandler(f_handler)  # <--

    newLogger.info("Logging initiated")  # Logging
    return newLogger


if __name__ == '__main__':
    logger: logging.Logger = initLogger()

    # Sending Hello to server
    msgFromClient = "Hello UDP Server"
    bytesToSend = str.encode(msgFromClient)
    serverAddressPortSend = (serverIP, serverPort)  # Server address

    # Create a UDP socket at client side
    UDPSocketSend = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)  # Socket to send commands

    # Send to server using created UDP socket
    UDPSocketSend.sendto(bytesToSend, serverAddressPortSend)

    # Initialise a thread for receiving grades from server (continuously)
    gradeReceiverThread = GradeReceiverThread(logger, UDPSocketSend, bufferSize)
    gradeReceiverThread.start()

    finishExec = False  # Flag to stop simulation (updated in method finishExecution() when needed)

    # using keyboard to control the drone. Can be changed
    keyboard.add_hotkey('w', forward, timeout=0)
    keyboard.add_hotkey('s', back, timeout=0)
    keyboard.add_hotkey('a', left, timeout=0)
    keyboard.add_hotkey('d', right, timeout=0)
    keyboard.add_hotkey('e', turnRight, timeout=0)
    keyboard.add_hotkey('q', turnLeft, timeout=0)
    keyboard.add_hotkey('page up', up, timeout=0)
    keyboard.add_hotkey('page down', down, timeout=0)
    keyboard.add_hotkey('space', hover, timeout=0)
    keyboard.add_hotkey('esc', finishExecution, timeout=0)  # Quitting the program when pressed

    # goto(x=-5.5, y=-5.9, z=-1.1, velocity=5.4, hasToFinish=True)
    # goto function is available but not bound to key

    while True:  # Checking for flag finishing the execution, otherwise a forever loop
        # Stops execution on 2 conditions: Either the command was received via the flag above, or the gradeReceiverThread has stopped
        if finishExec or not gradeReceiverThread.is_alive():
            # Send message to server to end simulation
            finishSimMessage = pickle.dumps(["finishedSim"])
            UDPSocketSend.sendto(finishSimMessage, serverAddressPortSend)
            logger.info("finishedSim sent")

            gradeReceiverThread.stop()
            UDPSocketSend.close()

            break

        time.sleep(2)
