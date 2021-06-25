import zmq
import time
import requests
import json
import schedule
import threading

threadKill = False

#receive data
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://benternet.pxl-ea-ict.be:24042")

#send data
push = context.socket(zmq.PUSH)
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

def getAirQ(param, topic):
    try:
        response = requests.get("https://docs.openaq.org/v2/latest?",params=param)
        if response.json()["meta"]["found"] == 0:
            return topic + ' ' + "de API kan je locatie niet vinden (controleer als je een hoofdletter hebt gebruikt) zo ja: dan heeft de API geen data van je stad"
        else:
            airData = {
            "city" : response.json()["results"][0]["city"],
            "parameter": response.json()["results"][0]["measurements"][0]["parameter"],
            "value" : response.json()["results"][0]["measurements"][0]["value"],
            "unit" : response.json()["results"][0]["measurements"][0]["unit"],
            }
            airDataJSON = json.dumps(airData)
            return topic + ' ' + airDataJSON

    except(requests.exceptions.RequestException, KeyError) as error:
        print("er is een error")
        pass
        return topic + ' ' + "error, er is een fout bij het data te requesten. controleer als je inputs correct zijn"

def threadFunc(topic,API,tijd):
    print("thread has been started")
    while not threadKill:
        if API == "weather":
            parsedData = {
                "query": "genk",
                "units": "m"
            }
            choices = ["uv_index"]
            data = getWeather(parsedData,choices,topic)
            print(data)
            push.send_string(data)
            time.sleep(tijd)
        elif API == "airQ":
            parsedData = {
                "limit": 1,
                "city": "Limburg",
            }
            data = getAirQ(parsedData,topic)
            print(data)
            push.send_string(data)
            time.sleep(tijd)

    print("thread has been killed")

def timedReq(topic,API,tijd):

    APIcallThread = threading.Thread(target=threadFunc, args=(topic,API,tijd))
    APIcallThread.start()



while True:
    try:
        socket.subscribe("weather")
        socket.subscribe("airQ")
        socket.subscribe("TIME")
        dataRecv = socket.recv_string()
        print(dataRecv)
        test = dataRecv.split("*")
        API = test[0]
        threadKill = False
        if API == "weather":
            if len(test[2]) != 0:
                choices = test[2].split(",")
            topic = test[4]

            parsedData = {
                "query" : test[1],
                "units" : test[3]
            }
            print(parsedData)
            weer = getWeather(parsedData,choices,topic)
            print(weer)
            push.send_string(weer)

        elif API == "airQ":
            parsedData = {
                "limit" : 1,
                "city" : test[1],
            }
            print(parsedData)
            airQuality = getAirQ(parsedData, test[2])
            print("AQ is:" + airQuality)

            push.send_string(airQuality)
        elif API == "TIME":
            print("in de time if")
            if test[4] == "starten":
                print("in de test if")
                timedReq(test[3],test[1],int(test[2]))
            elif test[4] == "stoppen":
                threadKill = True


    except IndexError:
        pass
    except zmq.ZMQError:
        print(zmq.ZMQError)
        push.send_string("er was een netwerk error start opnieuw.")
        continue
