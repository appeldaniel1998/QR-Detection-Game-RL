import os

import numpy as np
# ready to run example: PythonClient/car/hello_car.py
import airsim
import time
import cv2
import glob
import pandas as pd
import pathlib

if __name__ == '__main__':
    arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_1000)
    arucoParams = cv2.aruco.DetectorParameters_create()

    # connect to the AirSim simulator
    client = airsim.CarClient()
    client.confirmConnection()
    client.enableApiControl(True)
    car_controls = airsim.CarControls()

    # while True:
    #     # get state of the car
    #     car_state = client.getCarState()
    #     print("Speed %d, Gear %d" % (car_state.speed, car_state.gear))
    #
    #     # # set the controls for car
    #     # car_controls.throttle = 1
    #     # car_controls.steering = 1
    #     # client.setCarControls(car_controls)
    #     #
    #     # # let car drive a bit
    #     # time.sleep(1)
    #     #
    #     # get camera images from the car
    #     responses = client.simGetImages([
    #         airsim.ImageRequest(0, airsim.ImageType.DepthVis),
    #         airsim.ImageRequest(1, airsim.ImageType.DepthPlanar, True)])
    #     print('Retrieved images: %d', len(responses))
    #
    #     # do something with images
    #     for response in responses:
    #         if response.pixels_as_float:
    #             print("Type %d, size %d" % (response.image_type, len(response.image_data_float)))
    #             airsim.write_pfm('py1.pfm', airsim.get_pfm_array(response))
    #         else:
    #             print("Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
    #             airsim.write_file('py1.png', response.image_data_uint8)

    index = 0
    color = (0, 255, 0)
    thickness = 2
    while True:
        responses = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)])
        response = responses[0]

        # get numpy array
        img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8)

        # reshape array to 4 channel image array H X W X 4
        img_rgb = img1d.reshape(response.height, response.width, 3)

        # recognize qr codes
        (corners, ids, rejected) = cv2.aruco.detectMarkers(img_rgb, arucoDict, parameters=arucoParams)
        print(ids)

        try:
            corners = np.array(corners)
            corners = corners.astype(int)

            # rejected = np.array(rejected)
            # rejected = rejected.astype(int)

            image = img_rgb
            for i in range(len(corners)):
                image = cv2.line(image, tuple(corners[i][0][0]), tuple(corners[i][0][1]), color, thickness)
                image = cv2.line(image, tuple(corners[i][0][1]), tuple(corners[i][0][2]), color, thickness)
                image = cv2.line(image, tuple(corners[i][0][2]), tuple(corners[i][0][3]), color, thickness)
                image = cv2.line(image, tuple(corners[i][0][3]), tuple(corners[i][0][0]), color, thickness)
        except:
            pass
        cv2.imshow("", img_rgb)
        cv2.waitKey(1)  # wait 1 ms



        # write to png
        # airsim.write_png(os.path.normpath('testImg' + str(index) + '.png'), img_rgb)
        # index += 1
        # time.sleep(1)
