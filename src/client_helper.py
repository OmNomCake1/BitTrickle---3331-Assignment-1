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
        self.connectionSocket.send("Sending you files to download...\n".encode())
        self.connectionSocket.send("downloading....\n".encode())
        self.connectionSocket.send("download complete!".encode())
        self.connectionSocket.close()