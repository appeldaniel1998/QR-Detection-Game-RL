
import cv2
import numpy as np


def videoToImageList(srcVideoPath: str) -> list[np.ndarray]:
    """
    Function to turn a video into a list of images and save them to a folder
    :param srcVideoPath:
    :return:
    """
    imageLst = []
    vidcap = cv2.VideoCapture(srcVideoPath)
    success, currImg = vidcap.read()
    count = 0
    while success:
        imageLst.append(currImg)
        success, currImg = vidcap.read()
        count += 1
    print("Done reading video!")
    return imageLst


def detectArucoAndSaveVideoToFile(srcVideoPath: str, video_name: str) -> None:
    """
    Function to detect aruco codes in a video, mark them with squares and save the resulting video to a specified path
    :param srcVideoPath:
    :param video_name:
    :return:
    """
    images = videoToImageList(srcVideoPath)

    # Image list to detected video
    arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_1000)
    arucoParams = cv2.aruco.DetectorParameters_create()

    color = (0, 255, 0)
    thickness = 2

    for i in range(len(images)):
        # recognize qr codes

        try:
            (corners, ids, rejected) = cv2.aruco.detectMarkers(images[i], arucoDict, parameters=arucoParams)
            print(ids)

            corners = np.array(corners)
            corners = corners.astype(int)

            for j in range(len(corners)):  # Draw Corners
                images[i] = cv2.line(images[i], tuple(corners[j][0][0]), tuple(corners[j][0][1]), color, thickness)
                images[i] = cv2.line(images[i], tuple(corners[j][0][1]), tuple(corners[j][0][2]), color, thickness)
                images[i] = cv2.line(images[i], tuple(corners[j][0][2]), tuple(corners[j][0][3]), color, thickness)
                images[i] = cv2.line(images[i], tuple(corners[j][0][3]), tuple(corners[j][0][0]), color, thickness)
        except:
            pass

    video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), 30, (1920, 1080))

    for image in images:
        video.write(image)

    cv2.destroyAllWindows()
    video.release()


if __name__ == '_main_':
    detectArucoAndSaveVideoToFile("CarNoDetection.mp4", "video.mp4")
