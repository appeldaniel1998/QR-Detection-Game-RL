import airsim


class ArucoCode:
    playerStartPos = None  # Starting position of the drone (in UE4 coordinate system)
    ueIds = None  # IDs of the Aruco code objects in UE4
    airsimClient: airsim.MultirotorClient = None  # Airsim client

    def __init__(self, arucoId, xPos, yPos, zPos, movementAxis, movementStart, movementEnd):
        """
        :param: arucoId: Number the aruco represents (its ID)
        :param: xPos: X coordinate of the Aruco (in UE4 coordinate system)
        :param: yPos: Y coordinate of the Aruco (in UE4 coordinate system)
        :param: zPos: Z coordinate of the Aruco (in UE4 coordinate system)
        :param: movementAxis: movement axis of the Aruco (x, y, z or 0 (no movement)). Currently, only movement along 1 axis is supported
        :param: movementStart: coordinate (in UE4 coordinate system) of lower or upper bound of movement of the Aruco.
        :param: movementEnd: coordinate (in UE4 coordinate system) of the second bound of movement of the Aruco.
        """
        self.arucoId = arucoId
        self.xPos = xPos
        self.yPos = yPos
        self.zPos = zPos
        self.movementAxis = movementAxis
        self.movementStart = min(movementStart, movementEnd)
        self.movementEnd = max(movementStart, movementEnd)

        self.directionIsForward = True  # Flag to specify direction of movement of the Aruco

    def setAirsimPos(self, xPos, yPos, zPos):
        """
        Given x, y, z coordinates (in UE4 coordinate system), the method sets and moves the Aruco, converting to Airsim coordinate system, and setting the new position.
        The Method updates the current position of the Aruco code as well.
        :param: xPos: X coordinate (in UE4 coordinate system)
        :param: yPos: Y coordinate (in UE4 coordinate system)
        :param: zPos: Z coordinate (in UE4 coordinate system)
        :return:
        """
        self.xPos = xPos
        self.yPos = yPos
        self.zPos = zPos
        pose = ArucoCode.airsimClient.simGetObjectPose(ArucoCode.ueIds[str(self.arucoId)])  # Get current position of object. needed to keep the format identical
        pose.position.x_val = (xPos - ArucoCode.playerStartPos[0]) / 100  # Changing location -->
        pose.position.y_val = (yPos - ArucoCode.playerStartPos[1]) / 100
        pose.position.z_val = (zPos - ArucoCode.playerStartPos[2]) / -100  # <--
        ArucoCode.airsimClient.simSetObjectPose(ArucoCode.ueIds[str(self.arucoId)], pose)  # Set new location

    def move(self, moveBy: int):
        """
        The method moves the Aruco to its new place (if movable).
        The method uses and updates the  direction of movement of the Aruco code, as well as moving it by "moveBy" number of units in UE4 coordinate system
        :param: moveBy: number of units in UE4 coordinate system to move the Aruco code
        :return:
        """
        if self.movementAxis == "0":
            return

        elif self.movementAxis == "x":  # Move on X axis
            # If reached the end of its allowed movement, turn and move in the other direction
            if self.xPos + moveBy > self.movementEnd:  # Reached upper bound
                self.directionIsForward = False
            elif self.xPos - moveBy < self.movementStart:  # Reached lower bound
                self.directionIsForward = True

            # Move Aruco according to its direction
            if self.directionIsForward:
                self.setAirsimPos(self.xPos + moveBy, self.yPos, self.zPos)
            else:
                self.setAirsimPos(self.xPos - moveBy, self.yPos, self.zPos)

        elif self.movementAxis == "y":  # Move on Y axis
            # If reached the end of its allowed movement, turn and move in the other direction
            if self.yPos + moveBy > self.movementEnd:  # Reached upper bound
                self.directionIsForward = False
            elif self.yPos - moveBy < self.movementStart:  # Reached lower bound
                self.directionIsForward = True

            # Move Aruco according to its direction
            if self.directionIsForward:
                self.setAirsimPos(self.xPos, self.yPos + moveBy, self.zPos)
            else:
                self.setAirsimPos(self.xPos, self.yPos - moveBy, self.zPos)

        elif self.movementAxis == "z":  # Move on Z axis
            # If reached the end of its allowed movement, turn and move in the other direction
            if self.zPos + moveBy > self.movementEnd:  # Reached upper bound
                self.directionIsForward = False
            elif self.zPos - moveBy < self.movementStart:  # Reached lower bound
                self.directionIsForward = True

            # Move Aruco according to its direction
            if self.directionIsForward:
                self.setAirsimPos(self.xPos, self.yPos, self.zPos + moveBy)
            else:
                self.setAirsimPos(self.xPos, self.yPos, self.zPos - moveBy)
