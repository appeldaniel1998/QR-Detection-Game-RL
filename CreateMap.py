import airsim
import random
import json


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


def placeAruco(client: airsim.MultirotorClient, numberOfArucoToPlace: int, possibleLocations: list, ueIds: dict) -> airsim.MultirotorClient:
    """
    Function to randomly place a number (numberOfArucoToPlace) of aruco codes upon the map.
    The aruco codes placed are in range [1, numberOfArucoToPlace + 1], with no aruco having the same ID twice
    :param client: Airsim's client, imported from the main function where the connection to Airsim was made
    :param numberOfArucoToPlace: the number of aruco codes to place on the map. The number is originally imported from "mapConfig.json"
    :param possibleLocations: list of possible locations to place the Aruco codes. The places, too, are passed in "mapConfig.json".
    Each place specified has a scale to of aruco which is to be spawned
    :param ueIds: The IDs of the cubes upon which the aruco codes are located. Must match exactly to the IDs of the cubes in Unreal Engine
    (The IDs in UE are revealed upon mouse-hover over the name of the cube in the "World Outliner" section)
    :return: client upon which the changes are made
    """
    random.seed(0)  # random Seed
    for arucoId in range(1, numberOfArucoToPlace + 1):
        currRandomizedLocationID = random.randint(0, len(possibleLocations) - 1)  # Both inclusive
        chosenLocation = possibleLocations.pop(currRandomizedLocationID)

        position = client.simGetObjectPose(ueIds[arucoId])  # Get current position of object. needed to keep the format identical
        position.position.x_val = chosenLocation["xPos"]  # Changing location -->
        position.position.y_val = chosenLocation["yPos"]
        position.position.z_val = chosenLocation["zPos"]  # <--
        client.simSetObjectPose(ueIds[arucoId], position)  # Set new location

        scale = client.simGetObjectScale(ueIds[arucoId])  # Get old scale
        scale.x_val = chosenLocation["scaleX"]  # Change scale -->
        scale.y_val = chosenLocation["scaleY"]
        scale.z_val = chosenLocation["scaleZ"]  # <--
        client.simSetObjectScale(ueIds[arucoId], scale)  # Set new scale
    return client


def createMap(client: airsim.MultirotorClient) -> airsim.MultirotorClient:
    """
    Main function of the file. Calls relevant functions and passes them the relevant information, which is parsed from the "mapConfig.json" file
    :param client: Airsim's client, imported from the main function where the connection to Airsim was made
    :return: client upon which the changes are made
    """
    with open("CreatingConfigurationFiles/mapConfig.json", "r") as file:  # Read info from file
        mapConfig = json.load(file)

    loadWeather(client, mapConfig["weather"])
    placeAruco(client, mapConfig["numberOfArucoToSpawn"], mapConfig["PossibleCubePositions"], mapConfig["existingCubeNames"])
    return client
