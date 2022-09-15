# import the necessary packages
import numpy as np
import argparse
import cv2
import sys

if __name__ == '__main__':
    ARUCO_DICT = {
        "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
        "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
        "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
        "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
        "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
        "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
        "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
        "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
        "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
        "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
        "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
        "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
        "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
        "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
        "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
        "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
        "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
        "DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
        "DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
        "DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
        "DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
    }

    currId = 1
    size = 400
    border = 20

    # load the ArUCo dictionary
    arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT["DICT_4X4_100"])

    for i in range(currId, currId + 20):
        tag = np.zeros((size, size), dtype="uint8")
        cv2.aruco.drawMarker(arucoDict, i, size, tag, 1)
        tagWithBorder = np.zeros((size + 2 * border, size + 2 * border), dtype="uint8")
        tagWithBorder[:, :] = 255
        tagWithBorder[border:size + border, border:size + border] = tag

        # write the generated ArUCo tag to disk and then display it to our
        # screen
        cv2.imwrite('C:/Users/appel/PycharmProjects/pythonProject6/data' + str(i) + '.jpg', tagWithBorder)
