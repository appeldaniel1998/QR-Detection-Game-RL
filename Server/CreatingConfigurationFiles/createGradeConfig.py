import json

if __name__ == "__main__":
    toJsonDict = {
        "pointsAtStartOfGame": 0,
        "gameTime": 5 * 60,  # In seconds
        "pointsForQRDetected": 10,  # The number of points the agent receives upon detecting correctly an Aruco QR code
        "numberOfLives": 5,  # Number of times the drone can "die" before end of simulation
        "minusPointsPerSecInHeatZone": 1,
        "heatZoneRadius": 30,  # In meters
        "droneRecognitionRadius": 30  # Max distance of QR from drone which is to be recognized. In meters
    }

    with open("gradeConfig.json", "w") as file:
        json.dump(toJsonDict, file, indent=4)
