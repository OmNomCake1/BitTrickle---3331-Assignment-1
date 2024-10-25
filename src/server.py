# UDP indexing server for P2P network
# Written by Ryan Wong z5417983

import socket
import sys
import signal
from datetime import datetime, timedelta
import server_helper

credentials_path = 'credentials.txt'

# get port and host ip
if len(sys.argv) != 2:
    print("Expected usage: python3 server.py <port>")
    exit(0)
host = 'localhost'
port = int(sys.argv[1])
address = (host, port)

# parse credentials to dictionary
credentials = {}
with open(credentials_path, 'r') as file:
    for line in file:
        username, password = line.split()
        credentials[username] = password
        
# need to store
# 1. active peers
# 2. hearbeat time expected for each peer or something
# 3. which files are published and WHO published them (could be multiple)
# 4. list of peers and their TCP welcome sockets (if active)

# idea 1. a dictionary with keys = username
# and values of dictionary are instace of User class
# User class has attributes: is_active, [published_files], welcome_socket_port, timeout_time
# "dummy": server_helper.User(12001, datetime.now() + timedelta(seconds=3))
peers = {}
for user in credentials.keys():
    new_user = server_helper.User(0, datetime.now())
    peers[user] = new_user

# how to handle heartbeat
# if packet received is a heartbeat command, check who sent, get current time
# set is_active = true if not already
# set timeout_time = currentTime + 3 sec

# main loop
# 1. receive UDP packet - depending on what it wants (heartbeat/auth/sch/get) call that function
# 2. check all active user's timeout time by checking if current time > timeoutTime
        
# open UDP listening socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.bind(address)
serverSocket.settimeout(0.5)

print(f"Server listening on {port}...")

# function to gracefully shut down server
def server_shutdown(sig, frame):
    serverSocket.close()
    exit(0)

while (True):
    # handle ctrl-c to gracefully kill server
    signal.signal(signal.SIGINT, server_shutdown)
    
    # listen for packets
    try:
        data, client_address = serverSocket.recvfrom(1024)
        data_line_array = data.decode().split('\n')
        command, username = data_line_array[0].split()
        
        if command == "auth":
            # dont care about username cuz we already have it
            _, password, welcome_port = data_line_array[2].split()
            if server_helper.auth(peers, credentials, username, password, welcome_port):
                serverSocket.sendto(f"OK\n{datetime.now()}".encode(), client_address)
            else:
                serverSocket.sendto(f"ERR\n{datetime.now()}\nAuth failed: incorrect credentials or user already active".encode(), client_address)
            
    except socket.timeout:
        pass
    
    # Heartbeat handling
    # check active user's timeout_time
    for user in peers:
        if (peers[user].is_active):
            current_time = datetime.now()
            if current_time > peers[user].timeout_time:
                peers[user].is_active = False 
        print(user)
        peers[user].print_data()     
        print("")        
    print("---------------------------------")      

