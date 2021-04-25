import zmq


try:
    context = zmq.Context()
    #incoming messages
    sink = context.socket(zmq.PULL)
    sink.bind("tcp://127.0.0.1:5005")

    #outcoming messages
    publisher = context.socket(zmq.PUB)
    publisher.bind("tcp://127.0.0.1:5006")

    #linking one socket to another
    zmq.proxy(sink,publisher)

except Exception as e:
    print("er was een expection: " + e)


# ik heb de  https://github.com/zeromq/cppzmq
# hebruikt
# das de only header cpp bindings
# en das gewoon de zmq.hpp en zmq_addon.hpp toevoegen en je kunt verder
# ja
