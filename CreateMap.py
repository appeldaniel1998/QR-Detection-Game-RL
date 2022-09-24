import airsim
import random
import json


def loadWeather(client: airsim.MultirotorClient, weatherDict: dict) -> airsim.MultirotorClient:
    client.simEnableWeather(True)
    client.simSetWeatherParameter(airsim.WeatherParameter.Rain, weatherDict["rain"])
    client.simSetWeatherParameter(airsim.WeatherParameter.Snow, weatherDict["snow"])
    client.simSetWeatherParameter(airsim.WeatherParameter.Fog, weatherDict["fog"])
    client.simSetWeatherParameter(airsim.WeatherParameter.MapleLeaf, weatherDict["mapleLeaf"])
    client.simSetWeatherParameter(airsim.WeatherParameter.Dust, weatherDict["dust"])
    return client


def placeAruco(client: airsim.MultirotorClient, numberOfArucoToPlace: int, possibleLocations: list, ueIds: dict) -> airsim.MultirotorClient:
    random.seed(0)
    for arucoId in range(1, numberOfArucoToPlace + 1):
        currRandomizedLocationID = random.randint(0, len(possibleLocations) - 1)
        chosenLocation = possibleLocations.pop(currRandomizedLocationID)

        position = client.simGetObjectPose(ueIds[arucoId])
        position.position.x_val = chosenLocation["xPos"]
        position.position.y_val = chosenLocation["yPos"]
        position.position.z_val = chosenLocation["zPos"]
        client.simSetObjectPose(ueIds[arucoId], position)

        scale = client.simGetObjectScale(ueIds[arucoId])
        scale.x_val = chosenLocation["scaleX"]
        scale.y_val = chosenLocation["scaleY"]
        scale.z_val = chosenLocation["scaleZ"]
        client.simSetObjectScale(ueIds[arucoId], scale)
    return client


def createMap(client: airsim.MultirotorClient) -> airsim.MultirotorClient:
    with open("CreatingConfigurationFiles/mapConfig.json", "r") as file:
        mapConfig = json.load(file)

    loadWeather(client, mapConfig["weather"])
    placeAruco(client, mapConfig["numberOfArucoToSpawn"], mapConfig["PossibleCubePositions"], mapConfig["existingCubeNames"])
    return client
