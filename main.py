import sys

from Modules.api import API
from Modules.client import Client
from Modules.server import Server
from Models.neighbourmodel import NeighbourModel






if __name__ == '__main__':
    try:
        client = ""
        server = ""

        if sys.argv[1] != "":
            if sys.argv[1] == "client":
                neighbours = []
                neighbours.append(NeighbourModel(sys.argv[2], 6969, "empty"))
                client = Client(neighbours)
            elif sys.argv[1] == "server":
                server = Server(sys.argv[2], 6969)

    except KeyboardInterrupt:
        pass
    finally:
        if client != "":
            client.close()
        if server != "":
            server.close()
        print "Socket Closed"
