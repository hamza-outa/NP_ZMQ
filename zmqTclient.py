import zmq
import time
import os
import urllib.request

path_to_script = os.path.dirname(os.path.abspath(__file__))
my_filename = os.path.join(path_to_script, "bartIMAGE.png")

def userInput():
    nameAdres = input("vul je naam en stad in (spatie ertussen en in die volgorde):").split(" ")
    choices = input("vul je keuzes in (spaties ertussen): ").split(" ")
    parameters = input("vul je parameters in: ")

    dict = {
    "topic" : nameAdres[0],
    "adres": nameAdres[1],
    "choices": choices,
    "parameters" : parameters,
    }
    return dict

def createString(dataIn):
    concatChoices = ""
    str = "weather" + "*" + dataIn["adres"] + '*'
    for x in range(len(dataIn["choices"])):
        concatChoices = concatChoices + dataIn["choices"][x] + ','

    str = str + concatChoices + "*" + dataIn["parameters"] + '*'
    str = str + dataIn["topic"]
    return str

userData = userInput()
fullStr = createString(userData)

# sub connectie
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://benternet.pxl-ea-ict.be:24042")

#push connectie
push = context.socket(zmq.PUSH)
push.connect("tcp://benternet.pxl-ea-ict.be:24041")

push.send_string(fullStr)#API*location*temp,hum,weathDesc*param:units
#EXAMPLE: weather*harare*uv_index,humidity*m*hamza


socket.subscribe(userData["topic"])

# Receives a string format message
message = socket.recv_string()
print(message)

if userData["topic"] == "bart" or userData["topic"] == "Bart":
    print("in de folder waar deze script staat is een leuke png gespawned met de naam bartIMAGE.png")
    urllib.request.urlretrieve("http://11900456.pxl-ea-ict.be/fegtzqrgfrtsfd.png", my_filename)
