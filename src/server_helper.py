# helper functions and class for indexing server
# Includes a data class, one instance for each user 
from datetime import datetime, timedelta

# Data class for each user. Has the following fields:
# is_active, [published_files], welcome_socket_port, timeout_time
class User:
    """ 
    Data class for each user. Has the following fields:
    (bool) is_active, (string[]) [published_files], (string) welcome_socket_port, (datetime) timeout_time
    
    if is_active == false, welcome_socket_port, timeout_time is not valid (dont care)
    """
    
    def __init__(self, port, timeout_time):
        self.is_active = False
        self.published_files = []
        self.welcome_socket_port = port
        self.timeout_time = timeout_time
        
    # for debugging
    def print_data(self):
        print(f"is_active: {self.is_active}")
        print(f"published_files: {self.published_files}")
        print(f"welcome_socket_port: {self.welcome_socket_port}")
        print(f"timeout_time: {self.timeout_time}")
        

def auth(peers, credentials, username, password, port):
    """
    returns boolean signifying sucess/failed authentication
    need to also check - is user already active even if username/pass is correct
    also changes values of is_active = True, timeout_time = now + 3sec and welcome_socket_port if user successfully logs in 

    Args:
        peers (dictionary): dictionary of User objects
        credentials (dictionary): dictionary of correct username: passwords
        username (string): client sent username
        password (string): client sent password
        port (int): TCP welcome port of the client
    Return:
        bool: whether auth was successful or not
    """
    if username in credentials.keys() and credentials[username] == password:
        # check if peer already active
        if peers[username].is_active:
            return False
        
        # login
        peers[username].is_active = True
        peers[username].timeout_time = datetime.now() + timedelta(seconds=3)
        peers[username].welcome_socket_port = port
        return True
    else:
        # failed credential check
        return False


def get(client_username, peers, file_name):
    """
    get function which looks for if an ACTIVE peer has published a file, if it has, 
    returns true and tcp welcome port of that peer
    also does NOT include the querying peer

    Args:
        client_username (string): username of querying client
        peers (dctionary): dictionary of user objects
        file_name (string): exact file name to be downloaded

    Returns:
        (bool, int): a tuple of (was file found?, welcome socket)
    """
    found_file = False
    user_port = ""
    for user in peers.keys():
        if (peers[user].is_active and file_name in peers[user].published_files and user != client_username):
            found_file = True
            user_port = peers[user].welcome_socket_port
            
    return (found_file, user_port)


def lap(client_username, peers):
    """
    looks for the usernames of active peers, except the querying peer
    returns list of usernames

    Args:
        client_username (string): username of querying client
        peers (dictionary): dictionary of user objects

    Returns:
        array[string]: an array of active peer usernames
    """
    active_peers = []
    
    for user in peers.keys():
        if peers[user].is_active and user != client_username:
            active_peers.append(user)
    
    return active_peers