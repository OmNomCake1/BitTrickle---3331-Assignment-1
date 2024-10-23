import socket
import sys

address = 'localhost'

if (len(sys.argv) != 2):
    print("Expected usage: python3 server.py <port>")
    exit(0)

port = sys.argv[1]

print(port)