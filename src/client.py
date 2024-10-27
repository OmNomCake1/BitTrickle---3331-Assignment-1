import socket
import sys
from datetime import datetime
import signal
import threading
import time
import client_helper

# get host and ip
if len(sys.argv) != 2:
    print("Expected usage: python3 server.py <port>")
    exit(0)
host = 'localhost'
udp_port = int(sys.argv[1])
udp_address = (host, udp_port)

# function to gracefully shut down client
def client_shutdown(sig, frame):
    udpSocket.close()
    welcomeSocket.close()
    
# heartbeat thread function
def hbt_function(username):
    while(True):
        udpSocket.sendto(f"hbt {username}\n{datetime.now()}".encode(), udp_address)
        time.sleep(2)
        
# TCP welcome listenting thread function
def tcp_listen():
    welcomeSocket.listen()
    while(True):
        try:
            connectionSocket, peer_address = welcomeSocket.accept()
            # Spawn thread to handle downloading to one peer
            client_helper.PeerConnectionThread(peer_address, connectionSocket).start()
        except Exception as e:
            print(f"Error accepting TCP connection: {e}")
            break
        

# setup UDP socket
udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpSocket.settimeout(0.5)

# setup TCP welcome socket with RANDOM port, save the port it chose
welcomeSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
welcomeSocket.bind((host, 0))
tcp_port = welcomeSocket.getsockname()[1]

# authentication
print("=============================\nBitTrickle - COMP3331 Assignment\nWritten by: Ryan Wong z5417983 2024\n")
while (True):
    username = input("Username: ")
    password = input("Password: ")
    udpSocket.sendto(f"auth {username}\n{datetime.now()}\n{username} {password} {tcp_port}".encode(), udp_address)

    data, _ = udpSocket.recvfrom(1024)
    if "ERR" in data.decode():
        print("Authentication failed, please try again\n")
    elif "OK" in data.decode():
        print("\nLogin successful!\n\nWelcome to BitTrickle!!")
        print("Commands - get, lap, lpf, pub, sch, unp, xit")
        print(tcp_port)
        # start hbt thread
        hbt_thread = threading.Thread(target=hbt_function, daemon=True, name="Hbt thread", args=(username,))
        hbt_thread.start()
        # start tcp welcome listening thread
        tcp_welcome_thread = threading.Thread(target=tcp_listen, daemon=True, name="TCP welcome thread")
        tcp_welcome_thread.start()
        break
    else:
        # This should not happen... (for debugging purposes)
        print("Incorrect UDP server response structure...")
        exit(1)


# main interactive loop
while(True):
    com = input(">_ ")
    signal.signal(signal.SIGINT, client_shutdown)
    if com == "lpf":
        udpSocket.sendto(f"lpf {username}\n{datetime.now()}".encode(), udp_address)
    elif com == "pub":
        name = input("file: ")
        udpSocket.sendto(f"pub {username}\n{datetime.now()}\n{name}".encode(), udp_address)
    elif com == "sch":
        sub = input("substr: ")
        udpSocket.sendto(f"sch {username}\n{datetime.now()}\n{sub}".encode(), udp_address)
    elif com == "unp":
        name = input("file: ")
        udpSocket.sendto(f"unp {username}\n{datetime.now()}\n{name}".encode(), udp_address)
    elif com == "hbt":
        udpSocket.sendto(f"hbt {username}\n{datetime.now()}".encode(), udp_address)
    elif com == "get":
        # connect with another peer and receive file they are sending
        p = int(input("port: "))
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((host, p))
        full = ""
        # download all data from other peer
        try:
            while(True):
                data = clientSocket.recv(1024)
                if not data:
                    break
                
                message = data.decode()
                full += message
                
                if "complete" in message:
                    break
        except Exception as e:
            print(f"Error: {e}") 
        print(full)
        # close connection
        clientSocket.close()
                
    try:
        data, _ = udpSocket.recvfrom(1024)
        print(data.decode())
    except socket.timeout as e:
        pass

