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


def lpf(client_username, peers):
    """
    returns array of published files' names for client_username 

    Args:
        client_username (string): username of querying client
        peers (dictionary): dictionary of user objects

    Returns:
        array[string]: string array of published file names
    """
    return peers[client_username].published_files


def pub(client_username, peers, file_name):
    """
    appends given filename to peer object's published files list if it isnt in it already

    Args:
        client_username (string): username of querying client
        peers (dictionary): dictionary of user objects
        file_name (string): name of file wished to be published
    """
    if file_name not in peers[client_username].published_files:
        peers[client_username].published_files.append(file_name)
        
        
def sch(client_username, peers, sch_string):
    """
    returns a list of published file names which contain the given substring, 
    only if peer is active and not including querying peer

    Args:
        client_username (string): username of querying client
        peers (dictionary): dictionary of user objects
        sch_string (string): substring to be searched for

    Returns:
        array[string]: array of file names' strings which contain the substrubg
    """
    file_list = []
    for user in peers.keys():
        if user == client_username or not peers[user].is_active:
            continue
        for file in peers[user].published_files:
            if sch_string in file and file not in file_list:
                file_list.append(file)
    
    return file_list


def unp(client_username, peers, file_name):
    """
    removes given filename from client_username's published files list

    Args:
        client_username (string): querying client's username
        peers (dictionary): dictionary of user objects
        file_name (string): name of file to be unpublished

    Returns:
        _type_: _description_
    """
    if file_name not in peers[client_username].published_files:
        return False
    peers[client_username].published_files.remove(file_name)
    return True

def hbt(client_username, peers):
    """
    sets client's is_active to True if it wasn't already
    set new timeout_time to be now + 3 sec

    Args:
        client_username (string): username of querying client
        peers (dicitonary): dictionary of user objects
    """
    peers[client_username].is_active = True
    peers[client_username].timeout_time = datetime.now() + timedelta(seconds=3)
    