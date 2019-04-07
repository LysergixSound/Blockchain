import socket
import sys

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

            # Send data
            message = 'This is the message.  It will be repeated.'
            print >>sys.stderr, 'sending "%s"' % message
            self.sock.sendall(message)

            # Look for the response
            amount_received = 0
            amount_expected = len(message)

            while amount_received < amount_expected:
                data = sock.recv(16)
                amount_received += len(data)
                print >>sys.stderr, 'received "%s"' % data

        finally:
            print >>sys.stderr, 'closing socket'
            self.sock.close()


class Server:
    def __init__(self, ip, port):
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        self.server_address = (ip, port)
        print >>sys.stderr, 'starting up on %s port %s' % self.server_address
        self.sock.bind(self.server_address)

        # Listen for incoming connections
        self.sock.listen(1)

        # Start Connection Loop
        self.connection_loop()

    def close(self):
        self.sock.close()

    def connection_loop(self):
        while True:
            # Wait for a connection
            print >>sys.stderr, 'waiting for a connection'
            connection, client_address = self.sock.accept()

            try:
                print >>sys.stderr, 'connection from', client_address

                # Receive the data in small chunks and retransmit it
                while True:
                    data = connection.recv(16)
                    if data:
                        print >>sys.stderr, 'sending data back to the client'
                        connection.sendall(data)
                    else:
                        print >>sys.stderr, 'no more data from', client_address
                        break

            finally:
                # Clean up the connection
                connection.close()

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
