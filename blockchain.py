import socket
import sys
import time
from threading import Thread

class ClientModel:
    def __init__(self, id, address, connection):
        self.id = id
        self.address = address
        self.connection = connection

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
                message = 'heartbeat'
                print >>sys.stderr, 'sending "%s"' % message
                self.sock.sendall(message)

                time.sleep(2)

        finally:
            print >>sys.stderr, 'closing socket'
            self.sock.close()


class Server:
    def __init__(self, host, port):
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
                    response = data
                    print address[0] + ": " + response
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
