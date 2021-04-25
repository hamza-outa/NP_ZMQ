import zmq
import time
import requests
import json

#receive data
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://127.0.0.1:5006")

#send data
push = context.socket(zmq.PUSH)
push.connect("tcp://127.0.0.1:5005")
time.sleep(1)


#weer functie
def getWeather(param, choices, topic):
    param["access_key"] = "f52ea034c49d0999f230d1418631796b"
    response = requests.get("http://api.weatherstack.com/current?",params=param)

    weatherData = {
        "weatherDesc": response.json()["current"]["weather_descriptions"][0],
        "temperature": response.json()["current"]["temperature"],
    }

    for x in range(len(choices)-1):
        weatherData[choices[x]] = response.json()["current"][choices[x]]

    weatherDataJSON = json.dumps(weatherData)
    return topic + ' ' + weatherDataJSON

socket.subscribe("")
dataRecv = socket.recv_string()
print(dataRecv)
test = dataRecv.split("*")
API = test[0]
choices = test[2].split(",")
topic = test[4]

# test vorm is:
# test[0] = API
# test[1] = queryType
# test[2] = keuzes voor data
# test[3] = parameters
#test[4] = naam (topic)

parsedData = {
    "query" : test[1],
    "units" : test[3]
}

weer = getWeather(parsedData,choices,topic)
print(weer)
push.send_string(weer)
