import logging
import airsim
import random
import json
from ArucoCode import ArucoCode
from DynamicMap import DynamicMap


def loadWeather(client: airsim.MultirotorClient, weatherDict: dict) -> airsim.MultirotorClient:
    """
    Function to load all weather related parameters into the Airsim simulation
    :param client: Airsim's client, imported from the main function where the connection to Airsim was made
    :param weatherDict: Dictionary imported from JSON file "mapConfig.json", containing the relevant info to load
    :return: returns the client upon which the changes were made
    """
    client.simEnableWeather(True)
    client.simSetWeatherParameter(airsim.WeatherParameter.Rain, weatherDict["rain"])
    client.simSetWeatherParameter(airsim.WeatherParameter.Snow, weatherDict["snow"])
    client.simSetWeatherParameter(airsim.WeatherParameter.Fog, weatherDict["fog"])
    client.simSetWeatherParameter(airsim.WeatherParameter.MapleLeaf, weatherDict["mapleLeaf"])
    client.simSetWeatherParameter(airsim.WeatherParameter.Dust, weatherDict["dust"])
    return client


def placeAruco(client: airsim.MultirotorClient, numberOfArucoToPlace: int, possibleLocations: list, ueIds: dict, playerStartPos: list) -> (airsim.MultirotorClient, list):
    """
    Function to randomly place a number (numberOfArucoToPlace) of aruco codes upon the map.
    The aruco codes placed are in range [1, numberOfArucoToPlace + 1], with no aruco having the same ID twice
    :param client: Airsim's client, imported from the main function where the connection to Airsim was made
    :param numberOfArucoToPlace: the number of aruco codes to place on the map. The number is originally imported from "mapConfig.json"
    :param possibleLocations: list of possible locations to place the Aruco codes. The places, too, are passed in "mapConfig.json".
    Each place specified has a scale to of aruco which is to be spawned
    :param ueIds: The IDs of the cubes upon which the aruco codes are located. Must match exactly to the IDs of the cubes in Unreal Engine
    (The IDs in UE are revealed upon mouse-hover over the name of the cube in the "World Outliner" section)
    :param playerStartPos: starting position of player. To be used to transfer coordinates to Airsim units
    :return: client upon which the changes are made

    +X is north, +Y is east, +Z is down (according to Airsim Doc)
    """

    # random.seed(0)  # random Seed TODO: remove this line?
    arucos = []
    ArucoCode.playerStartPos = playerStartPos
    ArucoCode.ueIds = ueIds
    ArucoCode.airsimClient = client

    for arucoId in range(1, numberOfArucoToPlace + 1):  # For every Aruco
        currRandomizedLocationID = random.randint(0, len(possibleLocations) - 1)  # Both inclusive
        chosenLocation = possibleLocations.pop(currRandomizedLocationID)

        currAruco = ArucoCode(arucoId, chosenLocation["xPos"], chosenLocation["yPos"], chosenLocation["zPos"],
                              chosenLocation["movementAxis"], chosenLocation["movementStart"], chosenLocation["movementEnd"])
        arucos.append(currAruco)  # Add Aruco to a list to be returned  to the main function

        currAruco.setAirsimPos(chosenLocation["xPos"], chosenLocation["yPos"], chosenLocation["zPos"])  # Set stating location to the Aruco

        scale = client.simGetObjectScale(ueIds[str(arucoId)])  # Get old scale
        scale.x_val = chosenLocation["scaleX"]  # Change scale -->
        scale.y_val = chosenLocation["scaleY"]
        scale.z_val = chosenLocation["scaleZ"]  # <--
        client.simSetObjectScale(ueIds[str(arucoId)], scale)  # Set new scale
    return client, arucos


def createMap(client: airsim.MultirotorClient, logger: logging.Logger) -> (airsim.MultirotorClient, float):
    """
    Main function of the file. Calls relevant functions and passes them the relevant information, which is parsed from the "mapConfig.json" file
    :param logger: Logger object to enable logging
    :param client: Airsim's client, imported from the main function where the connection to Airsim was made
    :return: client upon which the changes are made
    """
    with open("CreatingConfigurationFiles/mapConfig.json", "r") as file:  # Read info from file
        mapConfig = json.load(file)

    loadWeather(client, mapConfig["weather"])

    client, arucos = placeAruco(client,
                                mapConfig["numberOfArucoToSpawn"],
                                mapConfig["PossibleCubePositions"],
                                mapConfig["existingCubeNames"],
                                mapConfig["PlayerStartPosition"])

    logger.info("Created map")  # Logging

    originArucoPos = mapConfig["originPosOfAruco"]  # Original position of the Aruco codes. To this location the arucos are to be transported after recognition (in place of despawn)
    originArucoPos["x"] = (originArucoPos["x"] - mapConfig["PlayerStartPosition"][0]) / 100
    originArucoPos["y"] = (originArucoPos["y"] - mapConfig["PlayerStartPosition"][1]) / 100
    originArucoPos["z"] = (originArucoPos["z"] - mapConfig["PlayerStartPosition"][2]) / -100

    dynamicMapThread = DynamicMap(arucos, logger)  # Initialize and start the dynamic map thread, which moves the arucos in real time
    dynamicMapThread.start()

    return client, mapConfig["numberOfArucoToSpawn"], originArucoPos, mapConfig["existingCubeNames"], dynamicMapThread
