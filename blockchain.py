import socket
import sys
import time
import threading
import json
import hashlib
from collections import namedtuple

from Modules.dotp2p import API
from Models.clientmodel import ClientModel
from Models.blockmodel import BlockModel




class Client:
    def __init__(self, ip, port):
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        self.server_address = (ip, port)
        print >>sys.stderr, 'connecting to %s port %s' % self.server_address
        self.sock.connect(self.server_address)

        self.send_data()

    def close(self):
        self.sock.close()

    def send_data(self):
        try:
            while True:
                # Send data
                hash_object = hashlib.sha256(b'genesis')
                hex_dig = hash_object.hexdigest()


                block = BlockModel(hex_dig, "testid", "hello", "", 0, 1)
                print block.toJSON()
                time.sleep(5)
                counter = 2
                while True:
                    proofResult = float.fromhex(hex_dig) * counter
                    proofResult = str(proofResult)
                    print proofResult[2:] + "\n"

                    tempResult = ""
                    for x in range(0, 1):
                        tempResult = tempResult + "0"

                    if proofResult[:1] == tempResult:
                        break

                    counter += 1
                    time.sleep(1)


                print >>sys.stderr, block.toJSON()
                self.sock.sendall(block)

                time.sleep(10)

        finally:
            print >>sys.stderr, 'closing socket'
            self.sock.close()


class Server:
    def __init__(self, host, port):
        self.nodes = []
        self.api = API(2)

        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.listen()

    def listen(self):
        self.sock.listen(1024)
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
                    block = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
                    print "Block is "
                    print self.api.verifiyData(block)
                else:
                    raise error('Client disconnected')
            except:
                client.close()
                return False




if __name__ == '__main__':
    try:
        client = ""
        server = ""

        if sys.argv[1] != "":
            if sys.argv[1] == "client":
                client = Client(sys.argv[2], 6969)
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
