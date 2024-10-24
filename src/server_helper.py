# helper functions and class for indexing server
# Includes a data class, one instance for each user 


# Data class for each user. Has the following fields:
# is_active, [published_files], welcome_socket_port, timeout_time
class User:
    def __init__(self, port, timeout_time):
        self.is_active = True
        self.published_files = []
        self.welcome_socket_port = port
        self.timeout_time = timeout_time
        
    # for debugging
    def print_data(self):
        print(f"is_active: {self.is_active}")
        print(f"published_files: {self.published_files}")
        print(f"welcome_socket_port: {self.welcome_socket_port}")
        print(f"timeout_time: {self.timeout_time}")