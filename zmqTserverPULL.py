import zmq
import time
import requests
import json

#weer functie
def getWeather(param, choices):
    param["access_key"] = "f52ea034c49d0999f230d1418631796b"
    response = requests.get("http://api.weatherstack.com/current?",params=param)

    weatherData = {
        "weatherDesc": response.json()["current"]["weather_descriptions"][0],
        "temperature": response.json()["current"]["temperature"],
    }

    for x in range(len(choices)):
        weatherData[choices[x]] = response.json()["current"][choices[x]]

    weatherDataJSON = json.dumps(weatherData)
    return weatherDataJSON



host = "127.0.0.1"
port = "5002"

# Creates a socket instance
context = zmq.Context()
socket = context.socket(zmq.PULL)

# Binds the socket to a predefined port on localhost
socket.bind("tcp://127.0.0.1:5002")
time.sleep(1)
dataRecv = socket.recv_string()

test = dataRecv.split("*")
API = test[0]
choices = test[2].split(",")

# test vorm is:
# test[0] = API
# test[1] = queryType
# test[2] = keuzes voor data
# test[3] = parameters

parsedData = {
    "query" : test[1],
    "units" : test[3]
}

print(getWeather(parsedData,choices))
