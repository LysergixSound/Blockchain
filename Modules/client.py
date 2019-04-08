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

        self.listen()
        self.test_send_data_loop()

    def listen(self):
        for neighbour in self.neighbours:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((neighbour.ip, neighbour.port))
            self.neighbourSockets.append(sock)
            threading.Thread(target = self.listenToServer,args = (sock)).start()

    def listenToServer(self, sock):
        size = 1024
        while True:
            try:
                data = sock.recv(size)
                if data:
                    self.api.ClientRequest(data)
                else:
                    raise error('Server disconnected')
            except:
                sock.close()
                return False

    def test_send_data_loop(self):
        while True:
            self.send_all("heartbeat")
            time.sleep(2)

    def send(self, sock, data):
        sock.sendall(data)

    def send_all(self, data):
        for sock in neighbourSockets:
            self.send(sock, data)

    def close(self):
        for sock in neighbourSockets:
            sock.close()
