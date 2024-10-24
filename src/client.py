import socket
import sys

# get host and ip
if len(sys.argv) != 2:
    print("Expected usage: python3 server.py <port>")
    exit(0)
host = 'localhost'
port = int(sys.argv[1])
address = (host, port)

# simply send stuff over UDP to the server as a tester
udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpSocket.sendto("hans falcon*solo".encode(), address)

while(True):
    pass

