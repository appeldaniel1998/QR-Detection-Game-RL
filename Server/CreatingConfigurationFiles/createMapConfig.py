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
                "yPos": 3040.0,
                "zPos": 920.0,
                "scaleX": 1.0,
                "scaleY": 1.0,
                "scaleZ": 1.0
            },
            {  # 2
                "xPos": 0.0,
                "yPos": 800.0,
                "zPos": 1320.0,
                "scaleX": 1.0,
                "scaleY": 1.0,
                "scaleZ": 1.0
            },
            {  # 3
                "xPos": 220.0,
                "yPos": 260.0,
                "zPos": 1550.0,
                "scaleX": 1.0,
                "scaleY": 1.0,
                "scaleZ": 1.0
            },
            {  # 4
                "xPos": 70.0,
                "yPos": -1990.0,
                "zPos": 1180.0,
                "scaleX": 1.0,
                "scaleY": 1.0,
                "scaleZ": 1.0
            },
            {  # 5
                "xPos": -510.0,
                "yPos": -2010.0,
                "zPos": 960.0,
                "scaleX": 0.25,
                "scaleY": 1.0,
                "scaleZ": 1.0
            },
            {  # 6
                "xPos": -310.0,
                "yPos": -2270.0,
                "zPos": 930.0,
                "scaleX": 1.0,
                "scaleY": 0.25,
                "scaleZ": 1.0
            },
            {  # 7
                "xPos": 330.0,
                "yPos": -2730.0,
                "zPos": 960.0,
                "scaleX": 0.25,
                "scaleY": 1.0,
                "scaleZ": 1.0
            },
            {  # 8
                "xPos": 1220.0,
                "yPos": -4330.0,
                "zPos": 990.0,
                "scaleX": 0.25,
                "scaleY": 1.0,
                "scaleZ": 1.0
            },
            {  # 9
                "xPos": 2970.0,
                "yPos": -3260.0,
                "zPos": 180.0,
                "scaleX": 1.0,
                "scaleY": 0.25,
                "scaleZ": 1.0
            },
            {  # 10
                "xPos": 3990.0,
                "yPos": -2910.0,
                "zPos": 620.0,
                "scaleX": 0.25,
                "scaleY": 0.75,
                "scaleZ": 0.75
            },
            {  # 11
                "xPos": 4715.168945,
                "yPos": 1488.005615,
                "zPos": 1194.794678,
                "scaleX": 1.0,
                "scaleY": 1.0,
                "scaleZ": 1.0
            },
            {  # 12
                "xPos": 4187.36377,
                "yPos": 5576.420898,
                "zPos": 1138.10376,
                "scaleX": 1.0,
                "scaleY": 1.0,
                "scaleZ": 1.0
            },
            {  # 13
                "xPos": 2990.0,
                "yPos": 6900.0,
                "zPos": 980.0,
                "scaleX": 1.0,
                "scaleY": 0.25,
                "scaleZ": 1.0
            },
            {  # 14
                "xPos": 2510.0,
                "yPos": 7210.0,
                "zPos": 930.0,
                "scaleX": 0.25,
                "scaleY": 1.0,
                "scaleZ": 1.0
            },
            {  # 15
                "xPos": 2490.0,
                "yPos": 7010.0,
                "zPos": 870.0,
                "scaleX": 0.25,
                "scaleY": 1.0,
                "scaleZ": 1.0
            },
            {  # 16
                "xPos": 400.0,
                "yPos": 5630.0,
                "zPos": 1290.0,
                "scaleX": 0.25,
                "scaleY": 1.0,
                "scaleZ": 1.0
            },
            {  # 17
                "xPos": 250.0,
                "yPos": 4670.0,
                "zPos": 1010.0,
                "scaleX": 1.0,
                "scaleY": 0.25,
                "scaleZ": 1.0
            },
            {  # 18
                "xPos": 2920.0,
                "yPos": 3080.0,
                "zPos": 920.0,
                "scaleX": 0.25,
                "scaleY": 1.0,
                "scaleZ": 1.0
            },
            {  # 19
                "xPos": 200.0,
                "yPos": 3210.0,
                "zPos": 300.0,
                "scaleX": 0.25,
                "scaleY": 1.0,
                "scaleZ": 1.0
            },
            {  # 20
                "xPos": 2010.0,
                "yPos": 590.0,
                "zPos": 980.0,
                "scaleX": 1.0,
                "scaleY": 1.0,
                "scaleZ": 0.75
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
        }
    }
    with open("mapConfig.json", "w") as file:
        json.dump(toJsonDict, file, indent=4)
