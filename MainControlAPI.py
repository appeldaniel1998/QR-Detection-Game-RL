import os

import numpy as np
# ready to run example: PythonClient/car/hello_car.py
import airsim
import time
import cv2
import glob
import pandas as pd
import pathlib

if __name__ == '_main_':
    # init airsim and drones
    client = airsim.MultirotorClient()  # connect to the simulator
    client.confirmConnection()
    client.reset()

    client.enableApiControl(True)  # enable API control on Drone0
    client.armDisarm(True)  # arm Drone0

    client.takeoffAsync().join()  # let Drone0 take-off
    client.moveToPositionAsync(0, 0, -1, 1).join()
    client.hoverAsync().join()

    vx = 0
    vy = 5
    vertical_speed = 0
    camera_heading = 180
    client.moveByVelocityAsync(vx, vy, vertical_speed, 1, airsim.DrivetrainType.MaxDegreeOfFreedom,
                               airsim.YawMode(False, camera_heading)).join()
    client.hoverAsync().join()

    state = client.getMultirotorState()
    print(state)

    collision = client.simGetCollisionInfo()
    print(collision)
