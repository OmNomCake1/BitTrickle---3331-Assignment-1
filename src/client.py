import socket
import sys
from datetime import datetime
import signal

# get host and ip
if len(sys.argv) != 2:
    print("Expected usage: python3 server.py <port>")
    exit(0)
host = 'localhost'
port = int(sys.argv[1])
address = (host, port)

# function to gracefully shut down client
def client_shutdown(sig, frame):
    udpSocket.close()
    exit(0)

# simply send stuff over UDP to the server as a tester
udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpSocket.settimeout(0.5)

while(True):
    com = input(">_ ")
    signal.signal(signal.SIGINT, client_shutdown)
    if com == "lpf":
        udpSocket.sendto(f"lpf hans\n{datetime.now()}".encode(), address)
    elif com == "pub":
        udpSocket.sendto(f"pub hans\n{datetime.now()}\nfunny_chimken.png".encode(), address)

    try:
        data, _ = udpSocket.recvfrom(1024)
        print(data.decode())
    except socket.timeout as e:
        pass
    

