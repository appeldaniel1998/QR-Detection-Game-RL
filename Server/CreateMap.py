import logging

import airsim
import random
import json
import pymap3d as pm


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
    geodeticArucoCoordinates = []
    originGPSCoordinates = client.getHomeGeoPoint()

    random.seed(0)  # random Seed

    for arucoId in range(1, numberOfArucoToPlace + 1):
        currRandomizedLocationID = random.randint(0, len(possibleLocations) - 1)  # Both inclusive
        chosenLocation = possibleLocations.pop(currRandomizedLocationID)

        position = client.simGetObjectPose(ueIds[str(arucoId)])  # Get current position of object. needed to keep the format identical
        position.position.x_val = (chosenLocation["xPos"] - playerStartPos[0]) / 100  # Changing location -->
        position.position.y_val = (chosenLocation["yPos"] - playerStartPos[1]) / 100
        position.position.z_val = (chosenLocation["zPos"] - playerStartPos[2]) / -100  # <--
        client.simSetObjectPose(ueIds[str(arucoId)], position)  # Set new location

        gpsCoordinateOfAruco = pm.enu2geodetic(position.position.y_val,  # Converting Airsim coordinate system to GPS coordinates
                                               position.position.x_val,
                                               -position.position.z_val,
                                               originGPSCoordinates.latitude,
                                               originGPSCoordinates.longitude,
                                               originGPSCoordinates.altitude)
        geodeticArucoCoordinates.append(gpsCoordinateOfAruco)

        scale = client.simGetObjectScale(ueIds[str(arucoId)])  # Get old scale
        scale.x_val = chosenLocation["scaleX"]  # Change scale -->
        scale.y_val = chosenLocation["scaleY"]
        scale.z_val = chosenLocation["scaleZ"]  # <--
        client.simSetObjectScale(ueIds[str(arucoId)], scale)  # Set new scale
    return client, geodeticArucoCoordinates


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

    client, geodeticArucoCoordinates = placeAruco(client,
                                                  mapConfig["numberOfArucoToSpawn"],
                                                  mapConfig["PossibleCubePositions"],
                                                  mapConfig["existingCubeNames"],
                                                  mapConfig["PlayerStartPosition"])

    logger.info("Created map")  # Logging

    originArucoPos = mapConfig["originPosOfAruco"]
    originArucoPos["x"] = (originArucoPos["x"] - mapConfig["PlayerStartPosition"][0]) / 100
    originArucoPos["y"] = (originArucoPos["y"] - mapConfig["PlayerStartPosition"][1]) / 100
    originArucoPos["z"] = (originArucoPos["z"] - mapConfig["PlayerStartPosition"][2]) / -100

    return client, mapConfig["numberOfArucoToSpawn"], geodeticArucoCoordinates, originArucoPos, mapConfig["existingCubeNames"]
