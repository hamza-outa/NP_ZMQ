# simple_sub.py
import zmq
import base64

# sub connectie
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://127.0.0.1:5001")

#push connectie
push = context.socket(zmq.PUSH)
push.connect("tcp://127.0.0.1:5002")
#temperature en weather description zijn standaard
push.send_string("weather*genk*uv index,humidity*m")      #API*location*temp,hum,weathDesc*param:units



socket.subscribe("")

# Receives a string format message
#message = socket.recv_string()
#print(message)
msgImg = socket.recv()
f = open("pastaTest.jpg","wb")
ba = bytearray(base64.b64decode(msgImg))
f.write(ba)
f.close()
