import socket
import sys
import threading

from Modules.api import API

class Server:
    def __init__(self, host, port):
        self.neighbours = []
        self.api = API(self, 4)
        self.listenLoop = False

        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.listen()

    def listen(self):
        self.listenLoop = True
        self.sock.listen(5)
        while self.listenLoop:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target = self.listenToClient,args = (client,address)).start()

    def listenToClient(self, client, address):
        size = 1024
        while True:
            try:
                data = client.recv(size)
                if data:
                    # Set the response to echo back the recieved data
                    # block = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
                    # print block
                    # print self.api.verifiyData(block)
                    self.api.serverRequest(data)
                    client.sendall(data)
                else:
                    raise error('Client disconnected')
            except:
                client.close()
                self.listenLoop = False
                return False

    def send(self, client, data):
        client.sendall(data)

    def send_all(self, data):
        self.sock.sendall(sock, data)

    def close(self):
        self.listenLoop = False
        self.sock.close()
