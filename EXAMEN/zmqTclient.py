import zmq
import time
import os
import urllib.request

path_to_script = os.path.dirname(os.path.abspath(__file__))
my_filename = os.path.join(path_to_script, "bartIMAGE.png")


def userInput():
    keuze = input("wil je weather, airquality of timer?:")
    if keuze == "weather" or keuze == "Weather":
        nameAdres = input("vul je naam en stad in (spatie ertussen en in die volgorde):").split(" ")
        choices = input("vul je keuzes in (spaties ertussen): ").split(" ")
        parameters = input("vul je parameters in: ")


        dict = {
        "topic" : nameAdres[0],
        "adres": nameAdres[1],
        "choices": choices,
        "parameters" : parameters,
        "API" : "weather",
        }

        if len(nameAdres) > 2:
            dict["adres"] = dict["adres"] + " " + nameAdres[2]

        return dict

    elif keuze == "airquality" or keuze == "Airquality":
        stad = input("welke stad wil je weten (MOET MET HOOFDLETTER BEGINNEN):")
        username = input("je username AUB:")
        dict = {
        "topic" : username,
        "adres" : stad,
        "API"   : "air",
        }
        return dict

    elif keuze == "timer" or keuze == "Timer":
        tijd = input("om de hoeveel seconden wil je de data:")
        while True:
            API = input("welke api wil je gebruiken (weather of airQ)")
            if API == "weather" or API == "airQ":
                break
            else:
                print("je moet kiezen tussen weather of airquality (type het tegoei AUB)")
                continue

        ID = input("vul een id in waarmee je de timer later wilt uitzetten:")
        actie = input("wil je starten of stoppen:")
        dict = {
        "topic" : ID,
        "time" : tijd,
        "keuze" : API,
        "API"  : "timer",
        "actie" : actie
        }
        return dict
    else:
        print("je moet kiezen tussen weather of airquality (zo geschreven zoals je hiernaast ziet)")
        exit()

def createStringAir(dataIn):
    str = "airQ" + "*" + dataIn["adres"] + "*" + dataIn["topic"]
    return str

def createStringWeather(dataIn):
    concatChoices = ""
    str = "weather" + "*" + dataIn["adres"] + '*'
    for x in range(len(dataIn["choices"])):
        concatChoices = concatChoices + dataIn["choices"][x] + ','

    str = str + concatChoices + "*" + dataIn["parameters"] + '*'
    str = str + dataIn["topic"]
    return str

def createStringTimer(dataIn):
    str = "TIME" + "*" + dataIn["keuze"] + "*" + dataIn["time"] + "*" + dataIn["topic"] + "*" + dataIn["actie"]
    return str



#---------------VANAF HIER BEGINT DE CODE---------------------
userData = userInput()
print(userData)
if userData["API"] == "weather":
    fullStr = createStringWeather(userData)
elif userData["API"] == "air":
    fullStr = createStringAir(userData)
elif userData["API"] == "timer":
    fullStr = createStringTimer(userData)
    print(fullStr)
else:
    print("fatal error at API descision. restart program")
    exit()
print(fullStr)
#exit()

# sub connectie
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://benternet.pxl-ea-ict.be:24042")

#push connectie
push = context.socket(zmq.PUSH)
push.connect("tcp://benternet.pxl-ea-ict.be:24041")




push.send_string(fullStr)
print(fullStr)



socket.subscribe(userData["topic"])


message = socket.recv_string()
print(message)

if userData["topic"] == "bart" or userData["topic"] == "Bart":
    print("in de folder waar deze script staat is een leuke png gespawned met de naam bartIMAGE.png")
    urllib.request.urlretrieve("http://11900456.pxl-ea-ict.be/fegtzqrgfrtsfd.png", my_filename)
