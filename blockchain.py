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
    def __init__(self, ip, port):
        # Init Lists
        self.threads = []

        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        self.server_address = (ip, port)
        print >>sys.stderr, 'starting up on %s port %s' % self.server_address
        self.sock.bind(self.server_address)

        # Start Connection Loop
        self.connection_loop()

    def close(self):
        self.sock.close()

    def connection_loop(self):
        idCounter = 0
        while True:
            # Listen for incoming connections
            self.sock.listen(1)

            # Wait for a connection
            connection, client_address = self.sock.accept()
            newClientThread = self.receiving_loop(ClientModel(str(idCounter), client_address, connection))
            newClientThread.start()
            self.threads.append(newClientThread)

            idCounter += 1
            print "client connected"

    def receiving_loop(self, client):
            try:
                # Receive the data in small chunks and retransmit it
                while True:
                    data = client.connection.recv(1024)
                    if data:
                        print >>sys.stderr, "Received " + client.address[0] + " ID:" + client.id + ": " + data
                    else:
                        print >>sys.stderr, 'no more data from', client.address
                        break

            finally:
                # Clean up the connection
                client.connection.close()




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
