import zmq
import time


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
queryType = test[1]
choices = test[2].split(",")
params = test[3]

parsedData = {
    "API" : test[0],
    "location" : test[1],
    "choices" : test[2].split(","),
    "units" : test[3]
}

print(parsedData)

time.sleep(1)
