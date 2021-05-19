import zmq
import time
import requests
import json

#receive data
context = zmq.Context()
socket = context.socket(zmq.SUB)
#socket.connect("tcp://127.0.0.1:5006")
socket.connect("tcp://benternet.pxl-ea-ict.be:24042")

#send data
push = context.socket(zmq.PUSH)
#push.connect("tcp://127.0.0.1:5005")
push.connect("tcp://benternet.pxl-ea-ict.be:24041")
time.sleep(1)


#weer functie
def getWeather(param, choices, topic):
    param["access_key"] = "f52ea034c49d0999f230d1418631796b"
    try:
        response = requests.get("http://api.weatherstack.com/current?",params=param)
        weatherData = {
            "weatherDesc": response.json()["current"]["weather_descriptions"][0],
            "temperature": response.json()["current"]["temperature"],
        }

        if choices[0] != "":
            for x in range(len(choices) - 1):
                weatherData[choices[x]] = response.json()["current"][choices[x]]

        weatherDataJSON = json.dumps(weatherData)
        return topic + ' ' + weatherDataJSON
    except (requests.exceptions.RequestException, KeyError) as error:
        print("er is een error")
        pass
        return topic + ' ' + "error, een van de inputs klopt niet. controleer als je een typfout hebt gemaakt"


while True:
    try:
        socket.subscribe("")
        dataRecv = socket.recv_string()
        print(dataRecv)
        test = dataRecv.split("*")
        API = test[0]
        if len(test[2]) != 0:
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

    except IndexError:
        pass
    except zmq.ZMQError:
        print(zmq.ZMQError)
        push.send_string("er was een netwerk error start opnieuw.")
        continue
