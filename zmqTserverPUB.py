
# simple_pub.py
import zmq
import time
import base64

# Creates a socket instance
context = zmq.Context()
socket = context.socket(zmq.PUB)

# Binds the socket to a predefined port on localhost
socket.bind("tcp://127.0.0.1:5001")

time.sleep(1)

# Sends a string message
#socket.send_string("play*playGame*fhjkshfdsjkfhsk")

f = open("pasta.jpg","rb")
bytes = bytearray(f.read())
strImg = base64.b64encode(bytes)
socket.send(strImg)
f.close()
