import json

if __name__ == "__main__":
    toJsonDict = {
        "numberOfArucoToSpawn": 2,
        "heatZoneSizeFromAruco": 100,  # heat zone size around the Aruco position.
        # To be checked against line of sight of the object. If drone is both in line of sight and in the box created,
        # it is said that it is "in the heat zone"
        "weather": {
            "rain": 0,
            "snow": 0,
            "mapleLeaf": 0,
            "dust": 0,
            "fog": 0
        },
        "PossibleCubePositions": [
            {
                "xPos": 0,
                "yPos": 0,
                "zPos": 0,
                "scaleX": 1,
                "scaleY": 1,
                "scaleZ": 1
            },
            {
                "xPos": 0,
                "yPos": 0,
                "zPos": 0,
                "scaleX": 1,
                "scaleY": 1,
                "scaleZ": 1
            },
            {
                "xPos": 0,
                "yPos": 0,
                "zPos": 0,
                "scaleX": 1,
                "scaleY": 1,
                "scaleZ": 1
            }
        ],
        "existingCubeNames": {  # the ids are to be identical as those in unreal engine 4. {arucoId: cubeId}
            1: "cube1",
            2: "cube2",
            3: "cube3"
        }
    }
    with open("mapConfig.json", "w") as file:
        json.dump(toJsonDict, file, indent=4)
