import socket
import sys
import threading
import time

from Modules.api import API
from Models.neighbourmodel import NeighbourModel


class Client:
    def __init__(self, neighbours):
        self.api = API(self, 4)
        self.neighbours = neighbours
        self.neighbourSockets = []
        self.listenLoop = False

        self.listen()

    def listen(self):
        self.listenLoop = True
        for neighbour in self.neighbours:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((neighbour.ip, neighbour.port))
            self.neighbourSockets.append(sock)
            threading.Thread(target = self.listenToServer,args = (sock, "")).start()

        while self.listenLoop:
            time.sleep(5)

    def listenToServer(self, sock, nonce):
        size = 1024
        while self.listenLoop:
            sock.sendall("heartbeat")
            try:
                data = sock.recv(size)
                print data
                if data:
                    self.api.ClientRequest(data)
                else:
                    raise error('Server disconnected')
            except:
                sock.close()
                return False

    def send(self, sock, data):
        sock.sendall(data)

    def send_all(self, data):
        for sock in self.neighbourSockets:
            self.send(sock, data)

    def close(self):
        self.listenLoop = False
        for sock in self.neighbourSockets:
            sock.close()
