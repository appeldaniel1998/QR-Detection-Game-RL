import airsim
from CreateMap import createMap
import numpy as np

if __name__ == '__main__':
    # init airsim and drones
    client = airsim.MultirotorClient()  # connect to the simulator
    client.confirmConnection()
    client.reset()

    client = createMap(client)

    client.enableApiControl(True)  # enable API control on Drone0
    client.armDisarm(True)  # arm Drone

    # client.simSetObjectMaterialFromTexture("testCube1_2", "C:/Users/appel/PycharmProjects/pythonProject6/ArucoImages/aruco1.jpg")

    # client.takeoffAsync().join()  # let Drone0 take-off
    # client.moveToPositionAsync(0, 0, -1, 1).join()
    # client.hoverAsync().join()
    #
    # xSpeed = 0
    # ySpeed = 5
    # zSpeed = 0  # Vertical
    # camera_heading = 180
    # client.moveByVelocityAsync(xSpeed, ySpeed, zSpeed, 1, airsim.DrivetrainType.MaxDegreeOfFreedom,
    #                            airsim.YawMode(False, camera_heading)).join()
    # client.hoverAsync().join()
    #
    # state = client.getMultirotorState()
    # print(state)
    #
    # collision = client.simGetCollisionInfo()
    # print(collision)
