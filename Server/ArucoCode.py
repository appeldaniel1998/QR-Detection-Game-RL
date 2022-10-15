import airsim


class ArucoCode:
    playerStartPos = None
    ueIds = None
    airsimClient: airsim.MultirotorClient = None

    def __init__(self, arucoId, xPos, yPos, zPos, movementAxis, movementStart, movementEnd):
        self.arucoId = arucoId
        self.xPos = xPos
        self.yPos = yPos
        self.zPos = zPos
        self.movementAxis = movementAxis
        self.movementStart = min(movementStart, movementEnd)
        self.movementEnd = max(movementStart, movementEnd)

        self.directionIsForward = True

    def setAirsimPos(self, xPos, yPos, zPos):
        self.xPos = xPos
        self.yPos = yPos
        self.zPos = zPos
        pose = ArucoCode.airsimClient.simGetObjectPose(ArucoCode.ueIds[str(self.arucoId)])  # Get current position of object. needed to keep the format identical
        pose.position.x_val = (xPos - ArucoCode.playerStartPos[0]) / 100  # Changing location -->
        pose.position.y_val = (yPos - ArucoCode.playerStartPos[1]) / 100
        pose.position.z_val = (zPos - ArucoCode.playerStartPos[2]) / -100  # <--
        ArucoCode.airsimClient.simSetObjectPose(ArucoCode.ueIds[str(self.arucoId)], pose)  # Set new location

    def move(self, moveBy: int):
        if self.movementAxis == "0":
            return

        elif self.movementAxis == "x":  # Move on X axis
            if self.xPos + moveBy > self.movementEnd:
                self.directionIsForward = False
            elif self.xPos - moveBy < self.movementStart:
                self.directionIsForward = True

            if self.directionIsForward:
                self.setAirsimPos(self.xPos + moveBy, self.yPos, self.zPos)
            else:
                self.setAirsimPos(self.xPos - moveBy, self.yPos, self.zPos)

        elif self.movementAxis == "y":  # Move on Y axis
            if self.yPos + moveBy > self.movementEnd:
                self.directionIsForward = False
            elif self.yPos - moveBy < self.movementStart:
                self.directionIsForward = True

            if self.directionIsForward:
                self.setAirsimPos(self.xPos, self.yPos + moveBy, self.zPos)
            else:
                self.setAirsimPos(self.xPos, self.yPos - moveBy, self.zPos)

        elif self.movementAxis == "z":  # Move on Z axis
            if self.zPos + moveBy > self.movementEnd:
                self.directionIsForward = False
            elif self.zPos - moveBy < self.movementStart:
                self.directionIsForward = True

            if self.directionIsForward:
                self.setAirsimPos(self.xPos, self.yPos, self.zPos + moveBy)
            else:
                self.setAirsimPos(self.xPos, self.yPos, self.zPos - moveBy)
