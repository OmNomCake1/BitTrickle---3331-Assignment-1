# helper functions and class for client.py
import threading

class PeerConnectionThread(threading.Thread):
    """
    A class which extends Thread. It basically handles connecting to a single peer in order to give them the filie
    run sends them the file
    """
    
    def __init__(self, peer_address, conenctionSocket):
        super().__init__() # init Thread class
        self.peer_address = peer_address
        self.connectionSocket = conenctionSocket

    def run(self):
        # receive file name which other client wants
        file_name = self.connectionSocket.recv(1024).decode()
            
        # open file to send
        send_file = open(file_name, "rb")
        entire_file = send_file.read()
        self.connectionSocket.sendall(entire_file)
        self.connectionSocket.close()