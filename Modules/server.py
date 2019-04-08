import socket
import sys
import threading

from Modules.api import API

class Server:
    def __init__(self, host, port):
        self.neighbours = []
        self.api = API(self, 4)

        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.listen()

    def listen(self):
        self.sock.listen(5)
        while True:
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
                else:
                    raise error('Client disconnected')
            except:
                client.close()
                return False

    def close(self):
        self.sock.close()
