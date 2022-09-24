import json

if __name__ == "__main__":
    toJsonDict = {
        "pointsAtStartOfGame": 0,
        "gameTime": 5 * 60,  # In seconds
        "timeForHeatZoneKill": 5,  # In seconds
        "pointsForQRDetected": 10  # The number of points the agent receives upon detecting correctly an Aruco QR code
    }

    with open("gradeConfig.json", "w") as file:
        json.dump(toJsonDict, file, indent=4)
