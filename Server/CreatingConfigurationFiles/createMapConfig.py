import json

if __name__ == "__main__":
    toJsonDict = {
        "numberOfArucoToSpawn": 10,
        "heatZoneSizeFromAruco": 30,  # heat zone size around the Aruco position.
        # To be checked against line of sight of the object. If drone is both in line of sight and within the radius,
        # it is said that it is "in the heat zone"
        "weather": {
            "rain": 0,
            "snow": 0,
            "mapleLeaf": 0,
            "dust": 0,
            "fog": 0
        },
        "PlayerStartPosition": [
            6162.900391,  # x coordinate
            -1914.331909,  # y coordinate
            188.961182,  # z coordinate
        ],
        "PossibleCubePositions": [
            {  # 1
                "xPos": 1260.0,
                "yPos": 3000.0,
                "zPos": 920.0,
                "scaleX": 1.0,
                "scaleY": 1.0,
                "scaleZ": 1.0,
                "movementAxis": "y",
                "movementStart": 3600,
                "movementEnd": 3000
            },
            {  # 2
                "xPos": -200.0,
                "yPos": 800.0,
                "zPos": 1320.0,
                "scaleX": 1.0,
                "scaleY": 1.0,
                "scaleZ": 1.0,
                "movementAxis": "x",
                "movementStart": 600,
                "movementEnd": -200
            },
            {  # 3
                "xPos": 150.0,
                "yPos": 260.0,
                "zPos": 1550.0,
                "scaleX": 1.0,
                "scaleY": 1.0,
                "scaleZ": 1.0,
                "movementAxis": "x",
                "movementStart": 450,
                "movementEnd": 150
            },
            {  # 4
                "xPos": 70.0,
                "yPos": -2150.0,
                "zPos": 1180.0,
                "scaleX": 1.0,
                "scaleY": 1.0,
                "scaleZ": 1.0,
                "movementAxis": "y",
                "movementStart": -2150,
                "movementEnd": -1700
            },
            {  # 5
                "xPos": -510.0,
                "yPos": -2010.0,
                "zPos": 960.0,
                "scaleX": 0.25,
                "scaleY": 1.0,
                "scaleZ": 1.0,
                "movementAxis": "0",
                "movementStart": 0,
                "movementEnd": 0
            },
            {  # 6
                "xPos": -310.0,
                "yPos": -2270.0,
                "zPos": 930.0,
                "scaleX": 1.0,
                "scaleY": 0.25,
                "scaleZ": 1.0,
                "movementAxis": "0",
                "movementStart": 0,
                "movementEnd": 0
            },
            {  # 7
                "xPos": 330.0,
                "yPos": -2600.0,
                "zPos": 960.0,
                "scaleX": 0.25,
                "scaleY": 1.0,
                "scaleZ": 1.0,
                "movementAxis": "y",
                "movementStart": -2600.0,
                "movementEnd": -3100
            },
            {  # 8
                "xPos": 1220.0,
                "yPos": -4330.0,
                "zPos": 990.0,
                "scaleX": 0.25,
                "scaleY": 1.0,
                "scaleZ": 1.0,
                "movementAxis": "0",
                "movementStart": 0,
                "movementEnd": 0
            },
            {  # 9
                "xPos": 2970.0,
                "yPos": -3260.0,
                "zPos": 200.0,
                "scaleX": 1.0,
                "scaleY": 0.25,
                "scaleZ": 1.0,
                "movementAxis": "z",
                "movementStart": 200,
                "movementEnd": 350
            },
            {  # 10
                "xPos": 3990.0,
                "yPos": -3000.0,
                "zPos": 620.0,
                "scaleX": 0.25,
                "scaleY": 0.75,
                "scaleZ": 0.75,
                "movementAxis": "y",
                "movementStart": -3000,
                "movementEnd": -2850
            },
            {  # 11
                "xPos": 4500.0,
                "yPos": 1490.0,
                "zPos": 1195.0,
                "scaleX": 1.0,
                "scaleY": 1.0,
                "scaleZ": 1.0,
                "movementAxis": "x",
                "movementStart": 4500,
                "movementEnd": 4900
            },
            {  # 12
                "xPos": 4190.0,
                "yPos": 5250.0,
                "zPos": 1140.0,
                "scaleX": 1.0,
                "scaleY": 1.0,
                "scaleZ": 1.0,
                "movementAxis": "y",
                "movementStart": 5250,
                "movementEnd": 5650
            },
            {  # 13
                "xPos": 2750.0,
                "yPos": 6900.0,
                "zPos": 980.0,
                "scaleX": 1.0,
                "scaleY": 0.25,
                "scaleZ": 1.0,
                "movementAxis": "x",
                "movementStart": 2750,
                "movementEnd": 3100
            },
            {  # 14
                "xPos": 2510.0,
                "yPos": 7300.0,
                "zPos": 930.0,
                "scaleX": 0.25,
                "scaleY": 1.0,
                "scaleZ": 1.0,
                "movementAxis": "y",
                "movementStart": 7300,
                "movementEnd": 7000
            },
            {  # 15
                "xPos": 2490.0,
                "yPos": 7300.0,
                "zPos": 870.0,
                "scaleX": 0.25,
                "scaleY": 1.0,
                "scaleZ": 1.0,
                "movementAxis": "y",
                "movementStart": 7300,
                "movementEnd": 7000
            },
            {  # 16
                "xPos": 400.0,
                "yPos": 5900.0,
                "zPos": 1290.0,
                "scaleX": 0.25,
                "scaleY": 1.0,
                "scaleZ": 1.0,
                "movementAxis": "y",
                "movementStart": 5900,
                "movementEnd": 5600
            },
            {  # 17
                "xPos": -150.0,
                "yPos": 4670.0,
                "zPos": 1010.0,
                "scaleX": 1.0,
                "scaleY": 0.25,
                "scaleZ": 1.0,
                "movementAxis": "x",
                "movementStart": -150,
                "movementEnd": 400
            },
            {  # 18
                "xPos": 2920.0,
                "yPos": 3400.0,
                "zPos": 920.0,
                "scaleX": 0.25,
                "scaleY": 1.0,
                "scaleZ": 1.0,
                "movementAxis": "y",
                "movementStart": 3400,
                "movementEnd": 2850
            },
            {  # 19
                "xPos": 200.0,
                "yPos": 3600.0,
                "zPos": 300.0,
                "scaleX": 0.25,
                "scaleY": 1.0,
                "scaleZ": 1.0,
                "movementAxis": "y",
                "movementStart": 3600,
                "movementEnd": 2500
            },
            {  # 20
                "xPos": 2010.0,
                "yPos": 500.0,
                "zPos": 980.0,
                "scaleX": 1.0,
                "scaleY": 1.0,
                "scaleZ": 0.75,
                "movementAxis": "y",
                "movementStart": 500,
                "movementEnd": 1450
            }
        ],
        "existingCubeNames": {  # the ids are to be identical as those in unreal engine 4. {arucoId: cubeId}
            1: "Cube_55",
            2: "Cube2_58",
            3: "Cube3_61",
            4: "Cube4_64",
            5: "Cube5_67",
            6: "Cube6_70",
            7: "Cube7_73",
            8: "Cube8_76",
            9: "Cube9_79",
            10: "Cube10_82"
        },
        "originPosOfAruco": {
            "x": 16810.0,
            "y": -5530.0,
            "z": 140.0
        }
    }
    with open("mapConfig.json", "w") as file:
        json.dump(toJsonDict, file, indent=4)
