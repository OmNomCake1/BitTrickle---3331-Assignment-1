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
    signal.signal(signal.SIGINT, client_shutdown)
    
    com = input(">_ ")
    if len(com) == 0:
        print("Invalid command... press h for help")
        
    elif com == "lpf":
        udpSocket.sendto(f"lpf {username}\n{datetime.now()}".encode(), udp_address)
        
    elif com == "lap":
        udpSocket.sendto(f"lap {username}\n{datetime.now()}".encode(), udp_address)
        
    elif com == "xit":
        print("Shutting down...")
        print("Goodbye!")
        udpSocket.close()
        welcomeSocket.close()
        exit(0)
        
    elif com.split()[0] == "pub" and len(com.split()) == 2: 
        file = com.split()[1]
        udpSocket.sendto(f"pub {username}\n{datetime.now()}\n{file}".encode(), udp_address)
        
    elif com.split()[0] == "sch" and len(com.split()) == 2:
        sub = com.split()[1]
        udpSocket.sendto(f"sch {username}\n{datetime.now()}\n{sub}".encode(), udp_address)
        
    elif com.split()[0] == "unp" and len(com.split()) == 2:
        file = com.split()[1]
        udpSocket.sendto(f"unp {username}\n{datetime.now()}\n{file}".encode(), udp_address)
        
    elif com.split()[0] == "get" and len(com.split()) == 2:
        file_wanted = com.split()[1]
        udpSocket.sendto(f"get {username}\n{datetime.now()}\n{file_wanted}".encode(), udp_address)
        
    elif com == "h":
        print("Commands - get, lap, lpf, pub, sch, unp, xit")
    else:
        print("Invalid command... press h for help")
    
    
    # receive response
    try:
        data, _ = udpSocket.recvfrom(1024)
        data = data.decode()
        
        if com == "lpf":
            if "ERR" in data:
                print("No files found")
            else:
                files = data.split('\n')[2]
                print(f"{len(files.split())} published files")
                print(files)
                
        elif com == "lap":
            if "ERR" in data:
                print("No other active peers")
            else:
                active_peers = data.split('\n')[2]
                print(f"{len(active_peers.split())} active peers:")
                print(active_peers)
            
        elif com.split()[0] == "pub" and len(com.split()) == 2: 
            # how I coded server, it can never return error (because assuming ideal scenario)
            print(f"File {com.split()[1]} successfully published")
            
        elif com.split()[0] == "sch" and len(com.split()) == 2:
            if "ERR" in data:
                print("No such file")
            else:
                files = data.split('\n')[2]
                print(f"{len(files.split())} files containing substring '{com.split()[1]}'")
                print(files)
                
        elif com.split()[0] == "unp" and len(com.split()) == 2:
            if "ERR" in data:
                print("No such file")
            else:
                print(f"File {com.split()[1]} successfully unpublished")
                
        elif com.split()[0] == "get" and len(com.split()) == 2:
            print(data)
            # clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # clientSocket.connect((host, p))
            # full = ""
            # # download all data from other peer
            # try:
            #     while(True):
            #         data = clientSocket.recv(1024)
            #         if not data:
            #             break
                    
            #         message = data.decode()
            #         full += message
                    
            #         if "complete" in message:
            #             break
            # except Exception as e:
            #     print(f"Error: {e}") 
            # print(full)
            # # close connection
            # clientSocket.close()
        
    except socket.timeout as e:
        pass

