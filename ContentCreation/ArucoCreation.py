import numpy as np
import cv2


def createQRAndSaveToFiles(path: str, numberOfAruco: int = 20, size: int = 400, whiteBorder: int = 20) -> None:
    """
    function to generate aruco codes with white borders around, and save them to a folder specified (has to exist)
    Aruco IDs are consecutive from 1
    :param numberOfAruco: Number of Aruco codes to generate
    :param path: Path to save the images
    :param size: Size of Images
    :param whiteBorder: Size of white border around Arucos
    :return:
    """
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

    currId = 1  # Starting aruco ID

    # load the ArUCo dictionary
    arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT["DICT_4X4_100"])

    for i in range(currId, currId + numberOfAruco):
        tag = np.zeros((size, size), dtype="uint8")
        cv2.aruco.drawMarker(arucoDict, i, size, tag, 1)
        tagWithBorder = np.zeros((size + 2 * whiteBorder, size + 2 * whiteBorder), dtype="uint8")
        tagWithBorder[:, :] = 255
        tagWithBorder[whiteBorder:size + whiteBorder, whiteBorder:size + whiteBorder] = tag

        cv2.imwrite(path + '/aruco' + str(i) + '.jpg', tagWithBorder)


if __name__ == '__main__':
    createQRAndSaveToFiles("/ArucoImages")
