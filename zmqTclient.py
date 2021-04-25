# simple_sub.py
import zmq
import base64
import time

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
socket.connect("tcp://127.0.0.1:5006")

#push connectie
push = context.socket(zmq.PUSH)
push.connect("tcp://127.0.0.1:5005")
#temperature en weather description zijn standaard
push.send_string(fullStr)      #API*location*temp,hum,weathDesc*param:units
#weather*harare*uv_index,humidity*m*hamza


socket.subscribe(userData["topic"])

# Receives a string format message
message = socket.recv_string()
print(message)


# msgImg = socket.recv()
# f = open("pastaTest.jpg","wb")
# ba = bytearray(base64.b64decode(msgImg))
# f.write(ba)
# f.close()
